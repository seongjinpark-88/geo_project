package lola

import java.io.File
import java.io._

import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.jackson.Serialization

import scala.collection.mutable

object LoLaExample extends App {
	implicit val formats = org.json4s.DefaultFormats
	// create the processor
	val geonorm = new org.clulab.geonorm.GeoLocationNormalizer(new org.clulab.geonorm.GeoNamesIndex(java.nio.file.Paths.get("./geonames-index")))

	val jsonSource = io.Source.fromURL(getClass.getResource("/new_interlim_result.json"))
	val json = parse(jsonSource.reader()).extract[mutable.HashMap[String, mutable.HashMap[String, Any]]]
	jsonSource.close()
	// println(Serialization.write(json))

//	println(Serialization.write(json("geoheritages_in_the").get("location")))
//	val newMap = parse(Serialization.write(json("geoheritages_in_the").get("location"))).extract[mutable.HashMap[String, Int]]
//	println(newMap)
//	println(newMap("East Asia"))

	val location_map = mutable.HashMap[String, mutable.HashMap[String, Float]]()

	for (k <- json.keysIterator){
		// val location_map = mutable.HashMap[String, Int]().withDefaultValue(0)
		// val freq_map = mutable.HashMap[String, Int]().withDefaultValue(0)
		// val id_map = mutable.HashMap[String, Int]()
		// val location_map = mutable.HashMap[String, mutable.Map[String, Int]]().withDefaultValue(mutable.Map[String, Int]().withDefaultValue(0))
		// val location_map = mutable.HashMap[String, info_map]()

		if (json(k) contains "location"){
			val newMap = parse(Serialization.write(json(k).get("location"))).extract[mutable.HashMap[String, Int]]
			for (loc <- newMap.keysIterator) {
				val new_site = geonorm(loc).head._1.name
				// val long = geonorm(loc).head._1.longitude
				// val lat = geonorm(loc).head._1.latitude

				// if (location_map notContains new_site){
					// location_map(new_site)("longitude") = long
					// location_map(new_site)("latitude") = lat
				// }
				// val new_id = geonorm(loc).head._1.id
				// location_map(new_site) += newMap(loc)
				// location_map(new_site)("frequency") += newMap(loc)	
				// info_map(new_site) += 
				// location_map(new_site)("id") = new_id.toInt
			}
		}
	}

	println(pretty(render(parse(Serialization.write(location_map)))))

	val writer = new FileWriter("LoLa.json", true)
	writer.write(pretty(render(parse(Serialization.write(location_map)))))
	
}



// 