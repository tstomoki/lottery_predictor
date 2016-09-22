# encoding: UTF-8


# this module is utilized for retriving the data
module DataGetter
  require 'nokogiri'
  require 'open-uri'
  require 'date'
  require 'pry'

  HEADER = ['Date', 'Location', 'Round',
            'Home', 'Away', 'Home Point', 'Away Point', 'Lottery Score']
  def whole_data
    base_uri = 'http://www.toto-dream.com/dci/I/IPB/IPB01.do'
    uri = base_uri << '?op=lnkLRLLotResultDettotoU'

    open(uri, 'r:Shift_JIS') do |data|
      doc = Nokogiri::HTML(data)
      main_table = doc.xpath('//*[@id="mainarea"]/table')[0]
      main_table.xpath('tr').each do |tr|
        round_info = tr.children.css('a')
        next if round_info.empty?
        round_info.map do |ri|
          round_str = ri.content
          round_uri = [base_uri, ri.attributes['href'].value].join
          p round_str, round_uri
        end
      end
    end
  end
  module_function :get_whole_data
end

DataGetter.get_whole_data
