package getlocation

import java.io.File
import java.io._

import jline.console.ConsoleReader
import jline.console.history.FileHistory
import org.clulab.odin.{Mention, ExtractorEngine}
import org.clulab.processors.{Document, Processor}
import org.clulab.processors.fastnlp.FastNLPProcessor
import org.clulab.processors.corenlp.CoreNLPProcessor
import utils._

import scala.collection.immutable.{HashMap, ListMap}
import scala.collection.mutable
import scala.collection.mutable.ListBuffer

object LocationExample extends App {

	// create the processor
  	// val fast: Processor = new FastNLPProcessor(useMalt = false, withDiscourse = false)
	val proc:Processor = new CoreNLPProcessor(withDiscourse = false)

	val file_sent = new File("Sentences.txt")
	val writer = new BufferedWriter(new FileWriter(file_sent))

	var sentenceCount = 0

	val bufferedSource = io.Source.fromURL(getClass.getResource("/text/Site.txt"))
	for (line <- bufferedSource.getLines) {
    
		val text = line.stripMargin
	  	
		val doc = proc.annotate(text)

		for (sentence <- doc.sentences) {
//			println("Sentence #" + sentenceCount + ":")
//			println(sentence.words.mkString(" "))
//			sentence.entities.foreach(entities => println(s"Named entities: ${entities.mkString(" ")}"))
			val entityString = sentence.entities.toList.flatten // mkString(" ").toList.toString
			if (entityString contains "LOCATION"){
			 	println("Sentence #" + sentenceCount + ":")
			 	println(sentence.words.mkString(" "))
				sentenceCount += 1
				println("\n")
				writer.write(sentence.words.mkString(" "))
			}
		}
		
	}
	bufferedSource.close
	writer.close()
}



