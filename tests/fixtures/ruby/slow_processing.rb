#!/usr/bin/env ruby
# Test fixture: Ruby file with processing logic

def batch_process(items)
  # Process array of items with map/reduce
  items.map { |x| x * 2 }.reduce(0, :+)
end

def crypto_operation(data)
  # Should recommend Rust for crypto
  require 'digest'
  Digest::SHA256.hexdigest(data.to_s)
end

def io_heavy_task(count)
  # I/O operations (should recommend Go for concurrency)
  results = []
  count.times do |i|
    results << i ** 2
  end
  results.sum
end

if __FILE__ == $PROGRAM_NAME
  if ARGV.empty?
    puts "READY"
  else
    val = ARGV[0].to_i
    result = batch_process((1..val).to_a)
    printf("%.15f\n", result.to_f)
  end
end
