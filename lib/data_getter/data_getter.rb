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
    def obtain_detail_data(round_str, uri)
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
            round_uri.match(/CntId=(\d+)/)
            round = $1.to_i
            p round
            detail_data = obtain_detail_data(round_str, round_uri)
            detail_data.map{|dd| dd[:Round] = round.to_i}
            ret_data.push detail_data
          end
        end
      end    
    end
  end
end

DataGetter.obtain_whole_data
