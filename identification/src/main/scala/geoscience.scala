package geoscience

import java.io.File
import java.io._

import jline.console.ConsoleReader
import jline.console.history.FileHistory

import org.clulab.odin.{Mention, ExtractorEngine} // Attachment
import org.clulab.processors.{Document, Processor}
// import org.clulab.processors.fastnlp.FastNLPProcessor
import org.clulab.processors.corenlp.CoreNLPProcessor

import utils._

import scala.collection.immutable.{HashMap, ListMap}
import scala.collection.mutable
import scala.collection.mutable.ListBuffer
import java.util.concurrent.ConcurrentHashMap

import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.jackson.Serialization

object GeoscienceExample extends App {

	implicit val formats = org.json4s.DefaultFormats


	// create the processor
	val fast: Processor = new CoreNLPProcessor(withDiscourse = false)

	// read rules from general-rules.yml file in resources
	val source = io.Source.fromURL(getClass.getResource("/grammars/geo_entities.yml"))
	val rules = source.mkString
	source.close()

	val jsonSource = io.Source.fromFile(args(0))
	val json = parse(jsonSource.reader()).extract[mutable.HashMap[String,mutable.HashMap[String, Any]]]

	jsonSource.close()

	val siteToLoc = new scala.collection.mutable.HashMap[String, String]()
	val siteLocDist = new scala.collection.mutable.HashMap[(String, String), Int]()

	val siteSource = io.Source.fromFile(args(1))
	
	for (l <- siteSource.getLines) {
		val t = l.stripMargin

		val Array(site, loc, dist) = t.split("\t")

		if (siteLocDist contains (site, loc)){
			if (dist.toInt < siteLocDist((site, loc))){
				siteToLoc(site) = loc
			}
		}
		else{ 
			siteToLoc(site) = loc
			siteLocDist((site, loc)) = dist.toInt
		}
		
	}

	siteSource.close()

	// Create Engine
	val extractor = ExtractorEngine(rules)
	val proc = fast

	val bufferedSource = io.Source.fromFile(args(2))

	for (line <- bufferedSource.getLines) {

		val counts = new scala.collection.mutable.HashMap[String, Int]()
    	// example sentence
		val newLine = line.split('\t')
		val label = newLine(0)
		val text = newLine(1).trim()

		val file_title = text.split(" +").slice(0, 5).mkString("_").replace("\"", "").toLowerCase

		// annotate the sentence
	  	
		val doc = proc.annotate(text)
	  	// extract mentions from annotated Document
		val mentions = extractor.extractFrom(doc)

		for (m <- mentions){

			if (m matches "SpatialExpr-Site") {
				if (siteToLoc contains m.text){

					val newSite = siteToLoc(m.text)

						if (counts contains newSite){
							counts(newSite) += 1
						} else {
							counts(newSite) = 1
						}

				}
				else {
	  				val newSite = m.text

					if (counts contains newSite){
						counts(newSite) += 1
					} else {
						counts(newSite) = 1
					}
				}
			}
			else if (m matches "SpatialExpr-Name") {

				if (counts contains m.text){
					counts(m.text) += 1
				} else {
					counts(m.text) = 1
				}

			}
		}

	  	
		for (sentence <- doc.sentences) {

			// list of NERs
			val entityList = sentence.entities.toList.flatten 
			// list of words
			val tokenList = sentence.words.toList
			// sentence
			val tokenString = tokenList.mkString(" ")
			// REGEX pattern
			
			// when LOCATION is recognized
			if ((entityList contains "LOCATION")) {

				// create empty list and string buffers
				val locations = ListBuffer[String]()
				val location = new StringBuilder("")

				// loop through entityList
				for (i <- 0 to entityList.length - 1) {
					val word = tokenList(i)

					// if no location has been recognized and this one is "LOCATION"
					if (location.toString == "" && entityList(i) == "LOCATION") {
						location ++= word
					}
					// if the previous one was also "LOCATION"
					else if (location.toString != "" && entityList(i) == "LOCATION") {
						location ++= " ".concat(word)
					}
					// end of recognizing "LOCATION"
					else if (location.toString != "" && entityList(i) != "LOCATION") {
						locations += location.toString

						// reset location
						location.setLength(0)
					}
				}

				// change ListBuffer to List
				val locationList = locations.toList

				// create count HashMap
				for (loc <- locationList) {

					if (counts contains loc){
						counts(loc) += 1
					} else {
						counts(loc) = 1
					}
				}

			}
		}

		json(file_title) += (("location", counts))
	}
	bufferedSource.close

	val writer = new FileWriter(args(3))

	writer.write(pretty(render(parse(Serialization.write(json)))))
	
	writer.close()
}



