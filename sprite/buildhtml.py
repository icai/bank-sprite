
# encoding: utf-8

import os
import urllib2
import ConfigParser
import time
class BuildBank(object):
	"""docstring for BuildBank"""

	all_bank = "ABC,ARCU,AYCB,BANKWF,BGB,BHB,BJBANK,BOC,BOCD,BOCY,BOD,BODD,BOJZ,BOP,BOQH,BOSZ,BOYK,BOZK,BSB,BZMD,CABANK,CBKF,CCB,CCQTGB,CDCB,CDRCB,CEB,CGNB,CIB,CITIC,CMB,CMBC,COMM,CQBANK,CRCBANK,CSCB,CSRCB,CZCB,CZCCB,CZRCB,DAQINGB,DBSCN,DLB,DRCBCL,DYCB,DYCCB,DZBANK,EGBANK,FJHXBC,FSCB,FXCB,GCB,GDB,GDRCC,GLBANK,GRCB,GSRCU,GXRCU,GYCB,GZB,GZRCU,H3CB,HANABANK,HBC,HBRCU,HDBANK,HKB,HNRCC,HNRCU,HSBANK,HSBC,HSBK,HURCB,HXBANK,HZCB,ICBC,JHBANK,JINCHB,JJBANK,JLRCU,JNBANK,JRCB,JSB,JSBANK,JXBANK,JXRCU,JZBANK,KLB,KSRB,LSBANK,LSBC,LSCCB,LZCCB,LZYH,NBBANK,NBYZ,NCB,NDHB,NHB,NJCB,NXBANK,NXRCU,NYCB,ORBANK,PSBC,PZHCCB,QDCCB,QLBANK,RZB,SCB,SCBBANK,SCCB,SCRCU,SDB,SDEB,SDRCU,SHBANK,SHRCB,SJBANK,SPABANK,SRBANK,SRCB,SXCB,SXRCCU,SZSBK,TACCB,TCCB,TCRCB,WHBANK,WHCCB,WHRCB,WJRCB,WRCB,WZCB,XABANK,XCYH,XLBANK,XTB,XXBANK,XYBANK,YBCCB,YNRCC,YQCCB,YXCCB,ZGCCB,ZJKCCB,ZJNX,ZJTLCB,ZRCBANK,ZYCBANK,ZZBANK"

	all_bank_list = all_bank.lower().split(',')
	# 所有银行列表 151 家
	def __init__(self, listtmpl,listbank,htmlpath = "bank.html" ,step = 40,pngurl = "bank_custom.png",isgetpng = True):
		super(BuildBank, self).__init__()
		self.listtmpl = listtmpl
		self.listbank = listbank

		self.htmlpath = htmlpath
		self.step = step 
		self.pngurl = pngurl
		if isgetpng == True : 
			self.getImg(self.all_bank)

		self.render()

	def getImg(self,banks):
		if os.path.isfile(self.pngurl) : return False

		#https://i.alipayobjects.com/combo.png?d=cashier&t=银行列表&stamp=1374163200000
		url="https://i.alipayobjects.com/combo.png?d=cashier&t="+ banks +"&stamp=1374163200000"
		headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"}
		imgRequest = urllib2.Request(url,headers=headers);
		imgData = urllib2.urlopen(imgRequest).read()
		output =open(self.pngurl,"wb") 
		output.write(imgData)
		output.close()

	def renderCss(self):
		banklist = self.all_bank_list
		step = self.step
		style = ""
		allbankclass = ""
		eachbankclass = ""
		allbankclass_tmpl = ".bank_{bank},"
		# 所有银行 class 名 集合 模板
		eachbankclass_tmpl = ".bank_{bank} {{ background-position: 0 {posy}; }} \n\t"
		# 单个银行  class 名 模板
		for i in  range(len(banklist)):
			allbankclass += allbankclass_tmpl.format(bank=banklist[i])
			eachbankclass += eachbankclass_tmpl.format(bank=banklist[i],posy=  str(- i * step) + "px" if i > 0 else str(- i * step)   )
		else :
			style = '''
			.bank_list li {
				float: left;
				padding: 10px 0;
				width: 180px;
				overflow: hidden;
			}
			.bank_list li .radio{
				float: left;
				margin: 8px 2px 0 2px;
			}
			.bank_list li .bank_label{ float: left; border:1px solid #e2e2e2; }
			.bank_list li .hover,.bank_list li .checked{
				border:1px solid #F60;
			}
			'''+allbankclass[:len(allbankclass) -1] + '''
			{ width: 126px;  height: 36px; background-image:url(
			'''+ self.pngurl + '''
			); background-repeat:no-repeat; cursor: pointer; display:block; }

			''' + eachbankclass
		return style

	def renderList(self,receivbank):
		body = ""
		for i in receivbank :
			body += self.listtmpl.format(bank=i)
		return body

	def render(self):
		style = self.renderCss()
		head = '''
		<!doctype html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<title>Document</title>
			<script src="http://code.jquery.com/jquery-1.7.2.js" ></script>
			<style>
		'''+ style +'''	
			</style>
		</head>
		<body>
			<ul class="bank_list" >
		'''
		foot = '''
			</ul>
			<script>
			$(function(){
				$('.bank_list .bank_label').hover(function(){
					$(this).addClass('hover');
				},function(){
					$(this).removeClass('hover');
				})
				$('input[type="radio"]').change(function(){
					var $id = $(this).attr('id'),$name = $(this).attr('name');
					$('label[for="'+ $id +'"]').addClass("checked").parents('li').siblings().find('label').removeClass('checked');
				})
			})
			</script>		
		</body>
		</html>
		'''
		body = self.renderList(self.listbank)
		f=open(self.htmlpath,"w") 
		f.write(head)
		f.write(body)
		f.write(foot)
		f.close()


################################################################

fasttmpl = '''<li>
	<input type="radio" name="qpbank" id="qpbank_{bank}" class="radio" value="qpbank_{bank}">
	<label  class="bank_label" for="qpbank_{bank}"><span class="bank_{bank}"></span></label>
</li>
'''
# 快捷支付模板


cd_tmpl = '''<li>
	<input type="radio" name="cdbank" id="cdbank_{bank}" class="radio" value="cdbank_{bank}">
	<label  class="bank_label" for="cdbank_{bank}"><span class="bank_{bank}"></span></label>
</li>
'''
#信用卡模板

################################################################

_list_cd = 'ICBC,BOC,CCB,CMB,ABC,SPABANK,SDB,CEB,GDB,CIB,CMBC,HXBANK,BJBANK,SHRCB,NXBANK,BOD,NBBANK,DLB,TCCB,BHB,JSBANK,HZCB,NJCB,HSBANK,WJRCB,CRCBANK,SRBANK,GZB,ZJTLCB,CZCB,GRCB,CDRCB,CSCB,BOJZ,HKB,NBYZ,DYCCB,SDEB,LZYH,BSB,BOQH,H3CB,JHBANK'
# list 银行列表 





###############################################################

def main():
	now = str(time.time() )
	path = "bank_alipay_"+ now +".html"
	pngPath = "bank_alipay_"+ now +".png"


	style = raw_input("please input your style in 'ini' file :")   #"default" 

	cf = ConfigParser.ConfigParser()
	cf.read("buildhtml.ini")

	tmpl = cf.get("template",style)
	banklist = cf.get("banklist",style)
	bank = banklist.lower().split(',')

	path = cf.get("main", "path") or path
	size = cf.getint("main", "size")
	pngPath = cf.get("main", "pngPath") or pngPath
	isgetpng =  cf.getboolean("main", "getpng")

	BuildBank(tmpl,bank,path,size,pngPath,isgetpng)

if __name__ == '__main__':
	main()
