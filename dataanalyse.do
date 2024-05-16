
global root = "D:\project\May2025_LRspider"
cd $root

/*
use keywords_year_count.dta
destring year ,replace force
keep if year == 2024
gsort -count
keep in 1/10
drop year
*/

**# 1.文献的演进历程

use lr.dta,clear
destring year ,replace force
drop if year == 2000
replace cited = 0 if cited == .
replace downloads = 0 if downloads == .
replace institure = subinstr(institure,";","",.)

gen x = 1
collapse (count) n = x,by(year)

tw (connect n year,mlab(n) mlabp(12)),  /// 
   xlabel(2008(2)2024) /// 
   ylabel(,nogrid) /// 
   xtitle(`"{fontface "宋体":年份}"') /// 
   ytitle(`"{fontface "宋体":"数字贸易"主题的CSSCI论文数（单位：篇）}"') /// 
   xline(2014,lp(shortdash)) /// 
   xline(2018,lp(shortdash)) /// 
   text(150 2011  `"{fontface "宋体":萌芽阶段}"') /// 
   text(150 2016  `"{fontface "宋体":发展阶段}"') /// 
   text(150 2021  `"{fontface "宋体":快速扩张阶段}"') /// 
   name(fig1,replace)
graph export "$root\output\fig1.png", as(png) name("fig1") replace



**# 2.发表刊物

/*
use lr.dta,clear
destring year ,replace force
drop if year == 2000
gen x = 1
collapse (count) n = x,by(year journal)

keep if year == 2023
gsort -n
drop year
keep in 1/10
*/

use lr.dta,clear
destring year ,replace force
drop if year == 2000
gen x = 1
collapse (count) n = x,by(journal)

gsort -n
keep in 1/20
gen ss = _n
replace journal = "国际商务" if journal == "国际商务(对外经济贸易大学学报)"

graph bar (sum) n ,over(journal,sort(ss) label(angle(45) labsize(small)) ) /// 
scheme(s1manual) ytitle(`"{fontface "宋体": 各CSSCI期刊发表“数字贸易”主题论文数}"')  /// 
name(fig2,replace) 
graph export "$root\output\fig2.png", as(png) name("fig2") replace

****

use lr.dta,clear
destring year ,replace force
merge m:1 journal using journaltype.dta
drop _m
gen tn = "综合类" if journal_type == 1
replace tn = "国贸专业类" if journal_type == 2
replace tn = "政策类" if journal_type == 3
replace tn = "其他专业类" if journal_type == 4

gen x = 1
collapse (count) n = x,by(tn year)
gen t = 1 if tn == "综合类"
replace t = 2 if tn == "国贸专业类" 
replace t = 3 if tn == "政策类"
replace t = 4 if tn == "其他专业类" 

keep if year >= 2014

tw (connect n year if t == 1 ,ms(oh)) /// 
   (connect n year if t == 2 ,ms(sh) lp(dash) ) /// 
   (connect n year if t == 3 ,ms(th)  lp(dash_dot)) /// 
   (connect n year if t == 4 ,ms(x) lp(shortdash)) , /// 
   xlabel(2014(2)2024) /// 
   ylabel(,nogrid) /// 
   xtitle(`"{fontface "宋体":年份}"') /// 
   ytitle(`"{fontface "宋体":"数字贸易"主题的CSSCI论文数（单位：篇）}"') /// 
   legend(col(4) label (1 `"{fontface "宋体": 综合类}"') /// 
   label (2 `"{fontface "宋体": 国贸专业类}"') /// 
   label (3 `"{fontface "宋体": 政策类}"') /// 
   label (4 `"{fontface "宋体": 其他专业类}"') ) /// 
   name(fig3,replace)
graph export "$root\output\fig3.png", as(png) name("fig3") replace
   





**# 3.机构

use lr.dta,clear
destring year ,replace force
replace institure = subinstr(institure,";","",.)
replace institure = "对外经济贸易大学中国WTO研究院" if inst == "对外经济贸易大学中国世界贸易组织研究院"
replace institure = "对外经济贸易大学国际经济贸易学院" if inst == "对外经济贸易大学国际经济与贸易学院;"

gen x = 1 
bys institure : egen n = count(x)
duplicates drop inst ,force
keep inst n
drop if inst == ""
gsort -n


***

use lr.dta,clear
destring year ,replace force
replace institure = subinstr(institure,";","",.)
replace institure = "对外经济贸易大学中国WTO研究院" if inst == "对外经济贸易大学中国世界贸易组织研究院"
replace institure = "对外经济贸易大学国际经济贸易学院" if inst == "对外经济贸易大学国际经济与贸易学院;"

gen x = 1 
bys institure year : egen n = count(x)
duplicates drop inst year ,force
keep inst n year 
drop if inst == ""
gsort -n
keep if year == 2024
drop year


**# 4.学者

use lr.dta,clear
destring year ,replace force

gen x = 1 
bys author_f : egen n = count(x)
duplicates drop author_f ,force
keep author_f n
drop if author_f == ""
gsort -n

*** 
use lr.dta,clear
destring year ,replace force

gen x = 1 
bys author_f year : egen n = count(x)
duplicates drop author_f year ,force
keep author_f year n
drop if author_f == ""
gsort -n
keep if year == 2024
drop year 




**# 文章类型

use lr.dta,clear
destring year ,replace force
merge m:n title using is_empirical.dta ,keep(match master) nogen norep
replace emp = 0 if emp == .
replace emp = 0 if title == "《数字资源贸易权益分享理论与实证》"

tab emp
gen x = 1
collapse (count) n = x  ,by(year emp)


reshape wide n,i(year) j(emp)
forv i = 0/1{
    replace n`i' = 0 if n`i' == .
}

keep if year >= 2008
gen n = n0 + n1
gen z = 0

tw (rarea z n0 year,fc(gs7%80)) /// 
   (rarea n0 n year,fc(gs11%80)), /// 
   legend(col(2) label (1 `"{fontface "宋体":定性研究}"') /// 
   label (2 `"{fontface "宋体":定量研究}"')) /// 
   xlabel(2008(2)2024) /// 
   ylabel(,nogrid) /// 
   xtitle(`"{fontface "宋体":年份}"') /// 
   ytitle(`"{fontface "宋体":"数字贸易"主题的CSSCI论文数（单位：篇）}"')  /// 
   name(fig4,replace )
graph export "$root\output\fig4.png", as(png) name("fig4") replace

graph bar (sum) n0 n1, over(year,label(angle(0))) stack percent /// 
      bar(1, color(gs7%80)) ///
	  bar(2, color(gs11%80)) /// 
	  legend(col(2) label (1 `"{fontface "宋体":定性研究}"') /// 
      label (2 `"{fontface "宋体":定量研究}"')) /// 
	  ytitle(`"{fontface "宋体":政策文与实证文占当年比重}"') /// 
	  name(fig5,replace ) xsize(34) ysize(20) 
graph export "$root\output\fig5.png", as(png) name("fig5") replace


keep year n0 n1 
xpose,clear var
order _
