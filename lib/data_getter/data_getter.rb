# encoding: UTF-8


# this module is utilized for retriving the data
module DataGetter
  class << self
    require 'nokogiri'
    require 'open-uri'
    require 'date'
    require 'pry'

    HEADER = ['Date', 'Location', 'Round',
              'Home', 'Away', 'Home Point', 'Away Point', 'Lottery Score']
    USER_AGENT = "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0"
    REFERER = "http://google.com"
    def obtain_detail_data(round_str, uri)
      open(uri, 'r:Shift_JIS',
           "User-Agent" => USER_AGENT,
           "Referer" => REFERER) do |data|
        sleep(1.0)        
        doc = Nokogiri::HTML(data)
        main_table = doc.xpath('//*[@id="mainarea"]/div[2]/div/table[1]')
        binding.pry
      end
    end
    
    def obtain_whole_data
      ret_data = []
      base_uri = 'http://www.toto-dream.com/dci/I/IPB/IPB01.do'
      uri = [base_uri, '?op=lnkLRLLotResultDettotoU'].join
      
      open(uri, 'r:Shift_JIS',
           "User-Agent" => USER_AGENT,
           "Referer" => REFERER) do |data|        
        doc = Nokogiri::HTML(data)
        main_table = doc.xpath('//*[@id="mainarea"]/table')[0]
        main_table.xpath('tr').each do |tr|
          round_info = tr.children.css('a')
          next if round_info.empty?
          round_info.map do |ri|
            round_str = ri.content
            round_uri = [base_uri, ri.attributes['href'].value].join
            obtain_detail_data(round_str, round_uri)
          end
        end
      end    
    end
  end
end

DataGetter.obtain_whole_data
