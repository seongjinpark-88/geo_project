package location_norm

import java.io.File
import java.io._

import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.jackson.Serialization

import scala.collection.mutable

object GeoLocationExample extends App {
	implicit val formats = org.json4s.DefaultFormats
	// create the processor
	val geonorm = new org.clulab.geonorm.GeoLocationNormalizer(new org.clulab.geonorm.GeoNamesIndex(java.nio.file.Paths.get("./geonames-index")))

	val jsonSource = io.Source.fromFile(args(0))
	val json = parse(jsonSource.reader()).extract[mutable.HashMap[String, mutable.HashMap[String, Any]]]
	jsonSource.close()

	for (k <- json.keysIterator){

		val location_map = mutable.HashMap[String, Int]().withDefaultValue(0)
		
		// when there are recognized locations
		if (json(k) contains "location"){
			val newMap = parse(Serialization.write(json(k).get("location"))).extract[mutable.HashMap[String, Int]]
			for (loc <- newMap.keysIterator) {
				val new_site = geonorm(loc).head._1.name
				// add the original frequency to the new key
				location_map(new_site) += newMap(loc)
			}
			json(k) -= "location"
			json(k) += (("location", location_map))
		}
	}

	println(pretty(render(parse(Serialization.write(json)))))

	// save the normalization result
	val writer = new FileWriter(args(1))
	writer.write(pretty(render(parse(Serialization.write(json)))))
	writer.close()
	
}



