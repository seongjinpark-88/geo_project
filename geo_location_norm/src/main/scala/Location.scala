package location_norm

import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.jackson.Serialization

import scala.collection.mutable

object GeoLocationExample extends App {
	implicit val formats = org.json4s.DefaultFormats
	// create the processor
	val geonorm = new org.clulab.geonorm.GeoLocationNormalizer(new org.clulab.geonorm.GeoNamesIndex(java.nio.file.Paths.get("./geonames-index")))

	val jsonSource = io.Source.fromURL(getClass.getResource("/frequency.json"))
	val json = parse(jsonSource.reader()).extract[mutable.HashMap[String, mutable.HashMap[String, Any]]]
	jsonSource.close()
	println(Serialization.write(json)

//	println(Serialization.write(json("geoheritages_in_the").get("location")))
//	val newMap = parse(Serialization.write(json("geoheritages_in_the").get("location"))).extract[mutable.HashMap[String, Int]]
//	println(newMap)
//	println(newMap("East Asia"))

	for (k <- json.keysIterator){
		val location_map = mutable.HashMap[String, Int]().withDefaultValue(0)
		val newMap = parse(Serialization.write(json(k).get("location"))).extract[mutable.HashMap[String, Int]]
		for (loc <- newMap.keysIterator) {
			val new_site = geonorm(loc).head._1.name
			location_map(new_site) += newMap(loc)
		}
		json(k) -= "location"
		json(k) += (("location", location_map))
	}

	println(pretty(render(parse(Serialization.write(json)))))
}



