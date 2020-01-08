package geoscience

import java.io.File

import jline.console.ConsoleReader
import jline.console.history.FileHistory

import org.clulab.odin.{Mention, ExtractorEngine} // Attachment
import org.clulab.processors.{Document, Processor}
import org.clulab.processors.fastnlp.FastNLPProcessor
// import org.clulab.geonorm.{GeoLocationNormalizer, GeoNamesIndex}

import utils._

import scala.collection.immutable.{HashMap, ListMap}
import scala.collection.mutable
import scala.collection.mutable.ListBuffer

import org.json4s.native.Json
import org.json4s.DefaultFormats

// case class AbsTime(year: Int) extends Attachment

object GeoscienceExample extends App {

	// create the processor
  	val fast: Processor = new FastNLPProcessor(useMalt = false, withDiscourse = false)
  	// val geonorm = new org.clulab.geonorm.GeoLocationNormalizer(new org.clulab.geonorm.GeoNamesIndex(java.nio.file.Paths.get("./src/main/resources/geonames-index")))

	// read rules from general-rules.yml file in resources
	val source = io.Source.fromURL(getClass.getResource("/grammars/geo_entities.yml"))
	val rules = source.mkString
	source.close()

	val siteToLoc = new scala.collection.mutable.HashMap[String, String]()

	val siteSource = io.Source.fromURL(getClass.getResource("/text/output.txt"))
	
	for (l <- siteSource.getLines) {
		val t = l.stripMargin

		val Array(site, loc, dist) = t.split("\t")

		siteToLoc(site) = loc
	}

	siteSource.close()


	val counts = new scala.collection.mutable.HashMap[String,Int]().withDefaultValue(0)

	// Create Engine
	val extractor = ExtractorEngine(rules)
	var proc = fast

	val bufferedSource = io.Source.fromURL(getClass.getResource("/text/sample_stim.txt"))
	
	for (line <- bufferedSource.getLines) {
    	// example sentence
		val text = line.stripMargin

		// annotate the sentence
	  	
	  	val doc = proc.annotate(text)

	  	// extract mentions from annotated Document
	  	val mentions = extractor.extractFrom(doc)

	  	for (m <- mentions){
	  		// displayMention(m)
	  		// println(s"${m.labels(0)} => ${m.text}")
	  		if (m matches "SpatialExpr-Site") {
	  			if (siteToLoc contains m.text){
	  				val newSite = siteToLoc(m.text)
	  				println(newSite)
	  				// geonorm(newSite) match {
	  				// 	case Success(normSite) => print(s"${m.text} => ${newSite} => ${normSite}")
	  				// 	case Failure(s) => print(s"Failure. Reason: $s")
	  				// }
	  				// val normSite = geonorm(newSite).head._1.name
	  				// print(s"${m.text} => ${newSite} => ${normSite}")
	  				counts(newSite) += 1
	  			}
	  			else {
	  				val newSite = m.text
	  				println(newSite)
	  				// val normSite = geonorm(newSite).head._1.name
	  				// locnorm(newSite, geonorm) match {
	  				// 	case Success(normSite) => print(s"${m.text} => ${newSite} => ${normSite}")
	  				// 	case Failure(s) => print(s"Failure. Reason: $s")
	  				// }
	  				// print(s"${m.text} => ${newSite} => ${normSite}")
	  				counts(newSite) += 1
	  			}
	  		}
	  		else if (m matches "SpatialExpr-Name") {
	  			println(m.text)
	  			// val normSite = geonorm(m.text).head._1.name
	  			counts(m.text) += 1
	  		}
	  	}

		// val intermediate_result = Json(DefaultFormats).write(counts)
		// println(intermediate_result)
	  	
// 	  	for (sentence <- doc.sentences) {
// //			println(sentence.words.mkString(" "))
// //			sentence.entities.foreach(entities => println(s"Named entities: ${entities.mkString(" ")}"))
// 			// list of NERs
// 			val entityList = sentence.entities.toList.flatten // mkString(" ").toList.toString
// 			// list of words
// 			val tokenList = sentence.words.toList
// 			// sentence
// 			val tokenString = tokenList.mkString(" ")
// 			// REGEX pattern
			
// 			// when LOCATION is recognized
// 			if ((entityList contains "LOCATION")) {

// 				// create empty list and string buffers
// 				val locations = ListBuffer[String]()
// 				val location = new StringBuilder("")

// 				// loop through entityList
// 				for (i <- 0 to entityList.length - 1) {
// 					val word = tokenList(i)

// 					// if no location has been recognized and this one is "LOCATION"
// 					if (location.toString == "" && entityList(i) == "LOCATION") {
// 						location ++= word
// 					}
// 					// if the previous one was also "LOCATION"
// 					else if (location.toString != "" && entityList(i) == "LOCATION") {
// 						location ++= " ".concat(word)
// 					}
// 					// end of recognizing "LOCATION"
// 					else if (location.toString != "" && entityList(i) != "LOCATION") {
// 						locations += location.toString

// 						// reset location
// 						location.setLength(0)
// 					}
// 				}

// 				// change ListBuffer to List
// 				val locationList = locations.toList

// 				// create count HashMap
// 				for (loc <- locationList) {
// 					val normSite = geonorm(loc)
// 	  				print(s"${loc} => ${normSite}")
// 					counts(loc) += 1
// 				}
// 			}
// 		}
	}
	bufferedSource.close


	// val final_result = Json(DefaultFormats).write(counts)
	// println(final_result)

	// def locnorm(location: String, geonorm:org.clulab.geonorm.GeoLocationNormalizer): Try[String] = Try {
	// 	return geonorm(location).head._1.name
	// }


	// def attachDate(mentions: Seq[Mention], date: Date): Seq[Mention] = {
	// 	for (m <- mentions) yield {
	// 		if (m matches "TimeExp") {
	// 			val newTime = m.text match {
	// 				case "million" => 1000000 - date
	// 			}
	// 			m.copy(attachments=Set(AbsTime(newTime)))
	// 		} else {
	// 			m
	// 		}
	// 	}
	// }
}



