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

// case class AbsTime(year: Int) extends Attachment

object GeoscienceExample extends App {

	implicit val formats = org.json4s.DefaultFormats


	// create the processor
	// val fast: Processor = new FastNLPProcessor(useMalt = false, withDiscourse = false)
	val fast: Processor = new CoreNLPProcessor(withDiscourse = false)

	// read rules from general-rules.yml file in resources
	val source = io.Source.fromURL(getClass.getResource("/grammars/geo_entities.yml"))
	val rules = source.mkString
	source.close()

	// val jsonSource = io.Source.fromURL(getClass.getResource("/new_time_result.json"))
	val jsonSource = io.Source.fromFile(args(0))
	val json = parse(jsonSource.reader()).extract[mutable.HashMap[String,mutable.HashMap[String, Any]]]

	jsonSource.close()

	val siteToLoc = new scala.collection.mutable.HashMap[String, String]()
	val siteLocDist = new scala.collection.mutable.HashMap[(String, String), Int]()

	// val siteSource = io.Source.fromURL(getClass.getResource("/text/output.txt"))
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


//	val counts = new scala.collection.mutable.HashMap[String,mutable.HashMap[String, mutable.HashMap[String, Int]]]()

	// Create Engine
	val extractor = ExtractorEngine(rules)
	val proc = fast

	// val bufferedSource = io.Source.fromURL(getClass.getResource("/new_result.txt"))
	val bufferedSource = io.Source.fromFile(args(2))

	for (line <- bufferedSource.getLines) {

		val counts = new scala.collection.mutable.HashMap[String, Int]()
    	// example sentence
		val newLine = line.split('\t')
		val label = newLine(0)
		val text = newLine(1).trim()
		// val (label, text) = line.stripMargin.split("\t")

		val file_title = text.split(" +").slice(0, 5).mkString("_").replace("\"", "").toLowerCase

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
//	  				println(newSite)
	  				// geonorm(newSite) match {
	  				// 	case Success(normSite) => print(s"${m.text} => ${newSite} => ${normSite}")
	  				// 	case Failure(s) => print(s"Failure. Reason: $s")
	  				// }
	  				// val normSite = geonorm(newSite).head._1.name
	  				// print(s"${m.text} => ${newSite} => ${normSite}")
						if (counts contains newSite){
							counts(newSite) += 1
						} else {
							counts(newSite) = 1
						}

				}
				else {
	  				val newSite = m.text
//	  				println(newSite)
	  				// val normSite = geonorm(newSite).head._1.name
	  				// locnorm(newSite, geonorm) match {
	  				// 	case Success(normSite) => print(s"${m.text} => ${newSite} => ${normSite}")
	  				// 	case Failure(s) => print(s"Failure. Reason: $s")
	  				// }
	  				// print(s"${m.text} => ${newSite} => ${normSite}")
					if (counts contains newSite){
						counts(newSite) += 1
					} else {
						counts(newSite) = 1
					}
				}
			}
			else if (m matches "SpatialExpr-Name") {
//	  			println(m.text)
	  			// val normSite = geonorm(m.text).head._1.name
				if (counts contains m.text){
					counts(m.text) += 1
				} else {
					counts(m.text) = 1
				}
//	  			counts(m.text) += 1
			}
		}

		// val intermediate_result = Json(DefaultFormats).write(counts)
		// println(intermediate_result)
	  	
		for (sentence <- doc.sentences) {
//			println(sentence.words.mkString(" "))
//			sentence.entities.foreach(entities => println(s"Named entities: ${entities.mkString(" ")}"))
			// list of NERs
			val entityList = sentence.entities.toList.flatten // mkString(" ").toList.toString
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
					// val normSite = geonorm(loc)
	  				// print(s"${loc} => ${normSite}")
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

//	val resultMap = new mutable.HashMap[String, mutable.Map[String, Int]]

//	val temMap = collection.mutable.Map(json.toMap.toSeq: _*)

//	resultMap("location") = counts
//	resultMap("time") = temMap


	//	resultMap.put("location", counts.toMap)
//	resultMap.put("time", json)

	// val final_result = Json(DefaultFormats).write(counts)
	// println(final_result)
	// println(Serialization.write(json))
	// val writer = new FileWriter("new_new_interlim_result.json", true)
	val writer = new FileWriter(args(3))

	// writer.write(Serialization.write(json))
	writer.write(pretty(render(parse(Serialization.write(json)))))
	
	writer.close()
	// println(pretty(render(Serialization.read(result))))
	// println(compact(render(counts)))
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



