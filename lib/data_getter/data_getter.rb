# encoding: UTF-8


# this module is utilized for retriving the data
module DataGetter
  class << self
    require 'nokogiri'
    require 'open-uri'
    require 'date'
    require 'pry'
    require 'pry-byebug'

    HEADER = ['Date', 'Location', 'Round',
              'Home', 'Score', 'Away', 'Result']
    USER_AGENT = "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0"
    REFERER = "http://google.com"
    BASE_URI = 'http://www.toto-dream.com/dci/I/IPB/IPB01.do'    
    def obtain_detail_data(uri)
      ret_array = []
      open(uri, 'r:Shift_JIS',
           "User-Agent" => USER_AGENT,
           "Referer" => REFERER) do |data|
        sleep(1.0)        
        doc = Nokogiri::HTML(data)
        main_table = doc.xpath('//*[@id="mainarea"]/div[2]/div/table[1]')[0]
        main_table.xpath('tr').each do |tr|
          game_info = tr.css('td')
          next if game_info.empty?
          insert_data = game_info.map{|gi| gi.content.strip}
          # block for less data
          next if HEADER.size != insert_data.size
          begin
            tmp_hash = [HEADER.map(&:to_sym), insert_data].transpose
            tmp_hash = Hash[*tmp_hash.flatten]
          rescue => e
            binding.pry
          end
          ret_array.push tmp_hash
        end
      end
      ret_array
    end

    def obtain_year_links(uri)
      open(uri, 'r:Shift_JIS',
           "User-Agent" => USER_AGENT,
           "Referer" => REFERER) do |data|
        doc = Nokogiri::HTML(data)
        year_info = doc.xpath('//*[@id="mainarea"]/div')[0]
        year_info = year_info.css('a').map{|yi| [yi.content, [BASE_URI, yi.attributes['href'].value].join]}
        # obtain current year
        current_year = doc.xpath('//*[@id="mainarea"]/h3')[0].content.strip
        year_info.unshift([current_year, uri])
        year_info
      end
    end
    
    def obtain_whole_data
      ret_data = []
      uri = [BASE_URI, '?op=lnkLRLLotResultDettotoU'].join
      
      year_info = obtain_year_links(uri)
      year_info.each do |year, year_uri|
        p year
        # get rounds in year
        open(year_uri, 'r:Shift_JIS',
             "User-Agent" => USER_AGENT,
             "Referer" => REFERER) do |data|        
          doc = Nokogiri::HTML(data)
          main_table = doc.xpath('//*[@id="mainarea"]/table')[0]
          main_table.xpath('tr').each do |tr|
            round_info = tr.children.css('a')
            next if round_info.empty?
            round_info.map do |ri|
              round_str = ri.content
              round_uri = [BASE_URI, ri.attributes['href'].value].join
              next unless round_uri.match(/CntId=(\d+)/)
              round = $1.to_i
              p round_str
              detail_data = obtain_detail_data(round_uri)
              year =~ %r{(\d+)}
              year_num = $~[1]
              detail_data.map{|dd| dd[:Round] = round.to_i; dd[:Date] = [year_num, dd[:Date]].join('/')}
              ret_data.push detail_data
            end
          end
        end
      end
      ret_data
    end
    
  end
end


if __FILE__ == $0
  whole_data = DataGetter.obtain_whole_data
  # write obtained data to JSON
  
end


