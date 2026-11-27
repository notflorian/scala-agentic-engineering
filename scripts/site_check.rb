# frozen_string_literal: true

require "json"
require "nokogiri"
require "pathname"
require "set"
require "uri"

directory, catalog, origin, baseurl = ARGV
abort "usage: ruby scripts/site_check.rb SITE CATALOG URL BASEURL" unless ARGV.length == 4

root = Pathname(directory).expand_path
chapters = JSON.parse(File.read(catalog))
locales = JSON.parse(File.read("site/_data/locales.json"))
navigation = JSON.parse(File.read("site/_data/navigation.json"))
groups = navigation.fetch("groups")
topics = navigation.fetch("topics")
errors = []
documents = {}

def normalize(text)
  text.gsub(/\s+/, " ").strip
end

def leaf_keys(value)
  value.flat_map do |key, child|
    child.is_a?(Hash) ? leaf_keys(child).map { |part| "#{key}.#{part}" } : key
  end.sort
end

def html_file(root, route)
  relative = route.delete_prefix("/")
  root.join(route.end_with?("/") ? relative + "index.html" : relative)
end

def alternatives(chapters, locale_chapter, origin, baseurl)
  equivalents = chapters.to_h do |lang, items|
    peer = items.find { |item| item.fetch("id") == locale_chapter.fetch("id") }
    [lang, origin + baseurl + peer.fetch("url")]
  end
  equivalents.merge("x-default" => equivalents.fetch("en"))
end

def make_search_entries(document, lang, page)
  headings = page.fetch("toc")
  container = document.at_css("#guide-text, .chapter-index")
  content = []
  heading = headings.first
  records = []
  save = lambda do
    title = heading.fetch("title").delete("`")
    title = page.fetch("title").delete("`") + " · " + title if heading != headings.first
    records << {lang: lang, url: "#{page.fetch('url')}##{heading.fetch('id')}", title: title,
                text: normalize(content.join(" "))}
  end
  container.element_children.each do |node|
    break if node["id"] == "chapter-index"

    if node.name.match?(/\Ah[1-6]\z/) && headings.any? { |item| item.fetch("id") == node["id"] }
      save.call if node["id"] != heading.fetch("id")
      heading = headings.find { |item| item.fetch("id") == node["id"] }
      content.clear
    else
      content.concat(node.xpath(".//text()").map(&:text))
    end
  end
  save.call
  records
end

# Parse and inventory each document before validating links.
root.glob("**/*.html").each do |path|
  route = "/" + path.relative_path_from(root).to_s.sub(/\Aindex\.html\z|(?<=\/)index\.html\z/, "")
  document = Nokogiri::HTML5(File.read(path), max_errors: 40)
  documents[route] = document
  document.errors.each { |error| errors << "#{route}: #{error.message.lines.first.strip}" }
  duplicates = document.css("[id]").map { |node| node["id"] }.tally.select { |_, count| count > 1 }
  errors << "#{route}: duplicate IDs #{duplicates.keys.join(', ')}" unless duplicates.empty?
end

landing = documents.fetch("/")
unless landing.at_css("html")["lang"] == "en" &&
       landing.at_css("link[rel=canonical]")["href"] == "#{origin}#{baseurl}/en/" &&
       landing.at_css("main a")["href"] == "#{baseurl}/en/"
  errors << "/: invalid English landing"
end

reference = File.binread("guide.md")
errors << "French download differs from guide.md" unless root.join("fr/guide.md").binread == reference

required_keys = leaf_keys(locales.fetch("en"))
locales.each do |lang, labels|
  valid_groups = labels.fetch("groups", {}).keys.sort == groups.keys.sort
  valid_topics = labels.fetch("topics", {}).keys.sort == topics.keys.sort
  errors << "#{lang}: missing UI translations" unless leaf_keys(labels) == required_keys && valid_groups && valid_topics
end

recovery = documents.fetch("/404.html").css(".recovery-links a").to_h { |node| [node["hreflang"], node["href"]] }
errors << "/404.html: missing language home links" unless
  recovery == chapters.transform_values { |items| baseurl + items.first.fetch("url") }

search_indexes = {}
expected_sitemap = {}
chapters.each do |lang, items|
  search_indexes[lang] = []
  errors << "#{lang}: missing Markdown download" if root.join(lang, "guide.md").size.zero?
  nav = items.map { |item| baseurl + item.fetch("url") }

  chapter_urls = nav.drop(1)
  by_id = items.to_h { |item| [item.fetch("id"), baseurl + item.fetch("url")] }
  errors << "#{lang}: navigation groups must include every chapter in order once" unless
    groups.values.flatten.map { |id| by_id[id] } == chapter_urls
  expected_topics = topics.transform_values { |topic| by_id.fetch(topic.fetch("chapter")) }

  items.each_with_index do |item, order|
    route = item.fetch("url")
    document = documents.fetch(route)
    canonical = origin + baseurl + route
    equivalents = alternatives(chapters, item, origin, baseurl)
    expected_sitemap[canonical] = equivalents
    errors << "#{route}: invalid language or main landmark" unless document.at_css("html")["lang"] == lang &&
      document.css("main#main-content").size == 1
    errors << "#{route}: missing title or description" if document.at_css("title").text.strip.empty? ||
      document.at_css("meta[name=description]")["content"].strip.empty?
    errors << "#{route}: invalid canonical" unless document.css("link[rel=canonical]").map { |node| node["href"] } == [canonical]
    alternate_nodes = document.css("link[rel=alternate][hreflang]")
    errors << "#{route}: invalid reciprocal alternates" unless alternate_nodes.size == equivalents.size &&
      alternate_nodes.to_h { |node| [node["hreflang"], node["href"]] } == equivalents
    switch = document.css(".locale-nav a").to_h { |node| [node["hreflang"], origin + node["href"]] }
    errors << "#{route}: locale selector changes chapter" unless switch == equivalents.reject { |key| key == "x-default" }
    nav_nodes = document.css("#chapter-nav a")
    errors << "#{route}: invalid navigation locale" unless nav_nodes.map { |node| node["href"] } == nav &&
      nav_nodes.select { |node| node["aria-current"] == "page" }.map { |node| node["href"] } == [baseurl + route]
    rendered_groups = document.css("#chapter-nav details[data-group]")
    errors << "#{route}: incorrect navigation groups" unless rendered_groups.map { |node| node["data-group"] } == groups.keys &&
      rendered_groups.all? do |node|
        node.css("a").map { |link| link["href"] } == groups.fetch(node["data-group"]).map { |id| by_id[id] } &&
          (!node.at_css('a[aria-current="page"]') || node.key?("open"))
      end

    if order.zero?
      cards = document.css(".topic-grid a[data-topic]")
      errors << "#{route}: incorrect homepage topics" unless cards.size == expected_topics.size &&
        cards.to_h { |link| [link["data-topic"], link["href"]] } == expected_topics
      errors << "#{route}: incorrect homepage chapter index" unless document.css(".home-index a").map { |link| link["href"] } == chapter_urls
    end

    expected_pagination = {}
    expected_pagination["prev"] = nav[order - 1] if order.positive?
    expected_pagination["next"] = nav[order + 1] if order + 1 < nav.size
    pagination = document.css(".chapter-pagination a")
    errors << "#{route}: incorrect chapter pagination" unless pagination.size == expected_pagination.size &&
      pagination.to_h { |link| [link["rel"], link["href"]] } == expected_pagination
    errors << "#{route}: invalid Markdown download link" unless
      document.css("a[download]").map { |link| link["href"] } == ["#{baseurl}/#{lang}/guide.md"]

    search = document.at_css("#local-search")
    errors << "#{route}: search index points to a different locale" unless search["data-index"] == "#{baseurl}/#{lang}/search.json"

    expected_ids = item.fetch("toc").map { |entry| entry.fetch("id") }
    container = document.at_css("#guide-text, .chapter-index")
    headings = container.css("h1,h2,h3,h4,h5,h6").reject { |node| node["id"] == "chapter-index" }
    errors << "#{route}: headings or stable anchors lost" unless headings.map { |node| node["id"] } == expected_ids &&
      headings.count { |heading| heading.name == "h1" } == 1
    errors << "#{route}: incorrect table of contents anchors" unless
      document.css(".guide-toc a").map { |link| link["href"] } == expected_ids.drop(1).map { |id| "##{id}" }
    french = documents.fetch(route.sub(%r{^/[^/]+/}, "/fr/")).at_css("#guide-text, .chapter-index")
    code = container.css("pre code").map(&:text)
    errors << "#{route}: rendered code differs from French" unless code == french.css("pre code").map(&:text)
    errors << "#{route}: rendered table structure differs from French" unless
      container.css("table").map { |table| table.css("tr").map { |row| row.css("th, td").size } } ==
      french.css("table").map { |table| table.css("tr").map { |row| row.css("th, td").size } }
    search_indexes[lang].concat(make_search_entries(document, lang, item))
  end
end

liquid_example = documents.fetch("/en/ch-15a/").css("pre code").map(&:text)
errors << "Liquid expressions were evaluated in the YAML example" unless liquid_example.any? do |code|
  code.include?('$' + '{{ github.sha }}')
end

sitemap = Nokogiri::XML(root.join("sitemap.xml").read) { |options| options.strict.nonet }
sitemap.remove_namespaces!
sitemap_urls = sitemap.xpath("/urlset/url")
actual_sitemap = sitemap_urls.to_h do |node|
  [node.at_xpath("loc").text, node.xpath("link").to_h { |alt| [alt["hreflang"], alt["href"]] }]
end
errors << "Sitemap locale coverage differs from canonical pages" unless sitemap_urls.size == expected_sitemap.size &&
  expected_sitemap == actual_sitemap
errors << "robots.txt must point to the deployed sitemap" unless
  root.join("robots.txt").read.lines.map(&:strip).include?("Sitemap: #{origin}#{baseurl}/sitemap.xml")

search_indexes.each do |lang, entries|
  errors << "#{lang}: search index contains a foreign locale" unless
    entries.all? { |entry| entry.fetch(:lang) == lang && entry.fetch(:url).start_with?("/#{lang}/") }
  root.join(lang, "search.json").write(JSON.generate(entries) + "\n")
end

# Verify local routes, files and fragments, including links produced from prose.
documents.each do |route, document|
  document.css("a[href], link[href], script[src], img[src]").each do |node|
    value = node["href"] || node["src"]
    next if value.empty? || value.start_with?("//") || value.match?(/\A(?:mailto|tel|data):/)

    begin
      url = URI.join(origin + baseurl + route, value)
    rescue URI::InvalidURIError
      errors << "#{route}: invalid URL #{value}"
      next
    end
    next unless "#{url.scheme}://#{url.host}#{url.port == url.default_port ? '' : ":#{url.port}"}" == origin

    if !baseurl.empty? && !url.path.start_with?("#{baseurl}/")
      errors << "#{route}: link escapes baseurl #{value}"
      next
    end
    target = URI::DEFAULT_PARSER.unescape(url.path.delete_prefix(baseurl))
    path = html_file(root, target)
    unless path.file?
      errors << "#{route}: broken link #{value}"
      next
    end
    next if url.fragment.nil? || url.fragment.empty?

    linked = documents[target]
    fragment = URI::DEFAULT_PARSER.unescape(url.fragment)
    errors << "#{route}: missing link fragment #{value}" unless linked && linked.css("[id]").any? { |node| node["id"] == fragment }
  end
end

abort errors.uniq.join("\n") unless errors.empty?

puts "#{expected_sitemap.size} indexable HTML pages · #{search_indexes.values.sum(&:size)} search sections · links, HTML, SEO and locale isolation verified"
