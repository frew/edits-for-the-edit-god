require 'pp'

filenames = File.open('metadata/enwiki-latest-md5sums.txt').map do |line|
  parts = line.strip.split
  parts[1]
end
filenames.select! {|url| url =~ /.*pages-meta-history.*7z/ }
urls = filenames.map do |filename|
  parts = filename.split('-')
  date = parts[1]
  "http://dumps.wikimedia.org/enwiki/#{date}/#{filename}"
end

File.open('metadata/links', 'w') do |file|
  urls.each do |url|
    file.puts url
  end 
end
