package cooccurrence

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

object CooccurrenceExample extends App {

	// create the processor
	val proc:Processor = new CoreNLPProcessor(withDiscourse = false)

	// read the sentences
	// val bufferedSource = io.Source.fromURL(getClass.getResource(args(0)))
	val bufferedSource = io.Source.fromFile(args(0))

	// create the counter
	val counts = new scala.collection.mutable.HashMap[(String, String),Int]().withDefaultValue(0)
	val dists = new scala.collection.mutable.HashMap[(String, String), ListBuffer[Int]]() {
   	override def apply(key: (String, String)) = super.getOrElseUpdate(key, ListBuffer())
	}

	// create the list for Sites and locations 
	val listSites = ListBuffer[String]()
	val listLocs = ListBuffer[String]()
	val listSamples = ListBuffer[String]()
	// loop through the lines
	for (line <- bufferedSource.getLines) {

		val text = line.stripMargin
		//		println(text)
		val tokens = text.split(" ")


		for (i <- 0 to tokens.length - 1) {
			if (tokens(i).matches("Site")) {

				var slice_start = 0
				var slice_end = tokens.length - 1

				if (i - 11 > 0) {
					slice_start = i - 11
				}

				if (i + 11 < tokens.length - 1) {
					slice_end = i + 11
				}

				val sampleString = tokens.toList.slice(slice_start, slice_end).mkString(" ")
				listSamples += sampleString
			}
		}
	}
	// close BufferedSource
	bufferedSource.close
//		println("number of samples: %d", listSamples.toList.length)


		// loop through the sentences
	for (sent <- listSamples.toList) {
		val doc = proc.annotate(sent)
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
			val pattern = "(IODP|DSDP|ODP)? Sites? U?[0-9]+[A-Z]?(, U?[0-9]+)?".r
			val siteList = pattern.findAllIn(tokenString).toList

			// when LOCATION is recognized
			if ((entityList contains "LOCATION")) {

				// capture Sites in the sentence
				val siteIndex = pattern.findAllMatchIn(tokenString).map(_.start).toList

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

						// map site, location, and their distance
						for (j <- 0 to siteList.length - 1) {
							val siteTrim = siteList(j).trim
//							printf("Site: %s, Location: %s, Distance: %d\n", siteTrim, location.toString, scala.math.abs(siteIndex(j) - i))
							dists(siteTrim, location.toString) += scala.math.abs(siteIndex(j) - i)

						}
						// reset location
						location.setLength(0)
					}
				}

				// change ListBuffer to List
				val locationList = locations.toList

				// create count HashMap
				for (site <- siteList) {
					val siteTrim = site.trim

					for (loc <- locationList) {
						counts(siteTrim, loc) += 1
						listSites += siteTrim
						listLocs += loc

					}
				}
			}
		}
	}
	
	// ROW and COLUMN for Matrix
	val uniqSites = listSites.toList.distinct
	val uniqLocs = listLocs.toList.distinct

	// create a matrix
	val comatrix = Array.ofDim[Int](uniqSites.length,uniqLocs.length)

	// fill the matrix
	for (((s, l), c) <- counts){
		val rowSite = uniqSites.indexOf(s)
		val columnLoc = uniqLocs.indexOf(l)

		comatrix(rowSite)(columnLoc) = c
	}

	val disambiguate = new scala.collection.mutable.HashMap[String, String]()
	// print Site - Location with MaxFreq
	for (i <- 0 to comatrix.length - 1) {
		val maxFreq = comatrix(i).max
		for (j <- 0 to comatrix(i).length - 1){
			if (comatrix(i)(j) == maxFreq){

				if (disambiguate.contains(uniqSites(i))){
					if (dists(uniqSites(i), uniqLocs(j)).toList.min < dists(uniqSites(i), disambiguate(uniqSites(i))).toList.min) {
						disambiguate(uniqSites(i)) = uniqLocs(j)
					}
				}
				else {
					disambiguate(uniqSites(i)) = uniqLocs(j)
				}

//				print(uniqSites(i))
//				print("\t")
//				print(uniqLocs(j))
//				print("\t")
//				print(dists(uniqSites(i), uniqLocs(j)).toList.min)
//				println()
			}
		}
	}

	val writer = new FileWriter(args(1), true)

	for ((k, v) <- disambiguate){
		val dist = dists(k, v).toList.min
		// printf("%s\t%s\t%d\n", k, v, dist)
		writer.write(s"${k}\t${v}\t${dist}\n")
	}
	writer.close()
}



