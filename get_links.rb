require 'pp'
require 'rubygems'
require 'mechanize'

latest_dir = 'http://dumps.wikimedia.org/enwiki/latest/'
a = Mechanize.new
a.get(latest_dir) do |page|
  canonical_urls = page.links.map {|link| URI.join(latest_dir, link.href).to_s }
  canonical_urls.select! {|url| url =~ /.*pages-meta-history.*7z/ }
  canonical_urls.each {|url| puts url}
end

