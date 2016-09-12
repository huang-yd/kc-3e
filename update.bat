set crawlerPath=G:\gongkechuang-3e\NLPPaperCrawler
set pdf2txtpath=G:\gongkechuang-3e\test\test\bin
set paperPath=G:\gongkechuang-3e\NLPPaperCrawler\PaperAnthology
set indexPath=G:\gongkechuang-3e\test\test\bin\index

python %crawlerPath%\NLPPaperCrawler_en.py %paperPath%
python %crawlerPath%\NLPPaperCrawler_en_forL.py %paperPath%
cd %pdf2txtpath%
java test.pdf2txt %paperPath%
java test.IndexFiles -docs %paperPath% -index %indexPath%
