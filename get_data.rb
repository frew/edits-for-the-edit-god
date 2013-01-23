require 'pp'

md5sums = {}
File.open('metadata/enwiki-latest-md5sums.txt').each do |line|
  parts = line.strip.split
  md5sums[parts[1]] = parts[0]
end
pp(md5sums)

File.open('metadata/links').each do |linkline|
  link = linkline.strip
  filename = link.split('/')[-1]
  filepath = 'data/' + filename
  if File.exists?(filepath) 
    puts "Found #{filepath}. Verifying."
    md5 = `md5sum #{filepath}`.split()[0]
    if md5 != md5sums[filename]
      puts "MD5 mismatch for #{filename}. Expected #{md5sums[filename]} but got #{md5}"
      exit(1)
    end
  else
    wgetcmd = "wget #{link} -O data/#{filename}" 
    system(wgetcmd)
  end
end
