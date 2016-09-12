package test;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

import org.apache.pdfbox.pdmodel.*;
import org.apache.pdfbox.text.PDFTextStripper;

public class pdf2txt {
	
	static void geText(Path file) throws IOException {
		// �Ƿ�����
		boolean sort = false;
		// pdf�ļ���
		String fileName = null;
		fileName = file.toAbsolutePath().toString();
		File pdfFile = new File(fileName);
		// �����ı��ļ�����
		String textFile = null;
		// ���뷽ʽ
		String encoding = "UTF-8";
		// ��ʼ��ȡҳ��
		int startPage = 1;
		// ������ȡҳ��
		int endPage = Integer.MAX_VALUE;
		// �ļ��������������ı��ļ�
		Writer output = null;
		// �ڴ��д洢��PDF Document
		PDDocument document = null;
		try {
			document = PDDocument.load(pdfFile);
			if (fileName.length() > 4) {
				textFile = fileName.substring(0, fileName.length() - 4 ) + ".txt";
				}
			File f = new File(textFile);
			if(!f.exists()){
				System.out.println("converting " + fileName + " to " + textFile);
				// �ļ���������д���ļ���textFile
				output = new OutputStreamWriter(new FileOutputStream(textFile), encoding);
				// PDFTextStripper����ȡ�ı�
				PDFTextStripper stripper = null;
				stripper = new PDFTextStripper();
				// �����Ƿ�����
				stripper.setSortByPosition(sort);
				// ������ʼҳ
				stripper.setStartPage(startPage);
				// ���ý���ҳ
				stripper.setEndPage(endPage);
				// ����PDFTextStripper��writeText��ȡ������ı�
				stripper.writeText(document, output);
				}
			else {
				System.out.println(textFile + " has been converted already.");
			}
			}
		catch (IOException e){
			//e.printStackTrace();
			}
		catch (IllegalArgumentException ilae){
			ilae.printStackTrace();
		}
		catch (NullPointerException npe){
			npe.printStackTrace();
		}
		finally {
			if (output != null) {
				// �ر������
				output.close();
				}
			if (document != null) {
				// �ر�PDF Document
				document.close();
				}
			}
		}
	
	static void getDirectoryText(Path path) throws IOException {
	    if (Files.isDirectory(path)) {
	      Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
	        @Override
	        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
	          try {
	            pdf2txt.geText(file);
	          } catch (IOException ignore) {
	            // don't index files that can't be read.
	          }
	          return FileVisitResult.CONTINUE;
	        }
	      });
	    } else {
	      pdf2txt.geText(path);
	    }
	  }
	
	public static void main(String[] args) {
		String docsPath = null;
		docsPath = args[0];
		final Path docDir = Paths.get(docsPath);
	    if (!Files.isReadable(docDir)) {
	      System.out.println("Document directory '" +docDir.toAbsolutePath()+ "' does not exist or is not readable, please check the path");
	      System.exit(1);
	    }
		try {
			pdf2txt.getDirectoryText(docDir);
		}
		catch (IOException e){
			e.printStackTrace();
		}
	}

}