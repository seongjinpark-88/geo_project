import org.clulab.odin._
import org.clulab.processors.{Sentence, Document}

package object utils {

  def displayMentions(mentions: Seq[Mention], doc: Document): Unit = {
    val mentionsBySentence = mentions groupBy (_.sentence) mapValues (_.sortBy(_.start)) withDefaultValue Nil
    for ((s, i) <- doc.sentences.zipWithIndex) {
      println(s"sentence #$i")
      println(s.getSentenceText)
      // println("Tokens: " + (s.words.indices, s.words, s.tags.get).zipped.mkString(", "))
      // printSyntacticDependencies(s)
      s.entities.foreach(entities => println(s"Named entities: ${entities.mkString(" ")}"))
      println

      val sortedMentions = mentionsBySentence(i).sortBy(_.label)
      val (events, entities) = sortedMentions.partition(_ matches "Event")
      val (tbs, rels) = entities.partition(_.isInstanceOf[TextBoundMention])
      val sortedEntities = tbs ++ rels.sortBy(_.label)
      println("entities:")
      sortedEntities foreach displayMention

      println
      println("events:")
      events foreach displayMention
      println("=" * 50)
    }
  }

  def printSyntacticDependencies(s:Sentence): Unit = {
    if(s.dependencies.isDefined) {
      println(s.dependencies.get.toString)
    }
  }

  def displayMention(mention: Mention) {
    val boundary = s"\t${"-" * 30}"
    println(s"${mention.labels} => ${mention.text}")
    println(boundary)
    println(s"\tRule => ${mention.foundBy}")
    val mentionType = mention.getClass.toString.split("""\.""").last
    println(s"\tType => $mentionType")
    println(boundary)
    mention match {
      case tb: TextBoundMention =>
        println(s"\t${tb.labels.mkString(", ")} => ${tb.text}")
      case em: EventMention =>
        println(s"\ttrigger => ${em.trigger.text}")
        displayArguments(em)
      case rel: RelationMention =>
        displayArguments(rel)
      case _ => ()
    }
    println(s"$boundary\n")
  }


  def displayArguments(b: Mention): Unit = {
    b.arguments foreach {
      case (argName, ms) =>
        ms foreach { v =>
          println(s"\t$argName ${v.labels.mkString("(", ", ", ")")} => ${v.text}")
        }
    }
  }

//  def time_to_era(time:Long) {
//    var real_era = ""
//    if (time <= 541000000 || time >= 4500000000){
//      real_era = "Precambrian"}
//    else if (time <= 4000000000 || time >= 6000000000){
//      real_era = "Hadean"
//    }
//    else if (time <= 2500000000 || time >= 4000000000){
//      real_era = "Archean"
//    }
//    else if (time <= 3600000000 || time >= 4000000000){
//      real_era = "Eoarchean"
//    }
//    else if (time <= 3200000000 || time >= 3600000000){
//      real_era = "Paleoarchean"
//    }
//    else if (time <= 2800000000 || time >= 3200000000){
//      real_era = "Mesoarchean"
//    }
//    else if (time <= 2500000000 || time >= 2800000000){
//      real_era = "Neoarch"
//    }
//    else if (time <= 541000000 || time >= 2500000000){
//      real_era = "Proterozoic"
//    }
//    else if (time <= 1600000000 || time >= 2500000000){
//      real_era = "Paleoproterozoic"
//    }
//    else if (time <= 2300000000 || time >= 2500000000){
//      real_era = "Siderian"
//    }
//    else if (time <= 2050000000 || time >= 2300000000){
//      real_era = "Rhyacian"
//    }
//    else if (time <= 1800000000 || time >= 2050000000){
//      real_era = "Orosirian"
//    }
//    else if (time <= 1600000000 || time >= 1800000000){
//      real_era = "Statherian"
//    }
//    else if (time <= 1000000000 || time >= 1600000000){
//      real_era = "Mesoproterozoic"
//    }
//    else if (time <= 1400000000 || time >= 1600000000){
//      real_era = "Calymmian"
//    }
//    else if (time <= 1200000000 || time >= 1400000000){
//      real_era = "Ectasian"
//    }
//    else if (time <= 1000000000 || time >= 1200000000){
//      real_era = "Stenian"
//    }
//    else if (time <= 541000000 || time >= 1000000000){
//      real_era = "Neoproterozoic"
//    }
//    else if (time <= 720000000 || time >= 1000000000){
//      real_era = "Tonian"
//    }
//    else if (time <= 635000000 || time >= 720000000){
//      real_era = "Cryogenian"
//    }
//    else if (time <= 541000000 || time >= 635000000){
//      real_era = "Ediacaran"
//    }
//    else if (time <= 251902000 || time >= 541000000){
//      real_era = "Paleozoic"
//    }
//    else if (time <= 251902000 || time >= 541000000){
//      real_era = "Palaeozoic"
//    }
//    else if (time <= 485400000 || time >= 541000000){
//      real_era = "Cambrian"
//    }
//    else if (time <= 443800000 || time >= 485400000){
//      real_era = "Ordovician"
//    }
//    else if (time <= 419200000 || time >= 443800000){
//      real_era = "Silurian"
//    }
//    else if (time <= 358900000 || time >= 419200000){
//      real_era = "Devonian"
//    }
//    else if (time <= 298900000 || time >= 358900000){
//      real_era = "Carboniferous"
//    }
//    else if (time <= 251902000 || time >= 298900000){
//      real_era = "Permian"
//    }
//    else if (time <= 66000000 || time >= 251902000){
//      real_era = "Mesozoic"
//    }
//    else if (time <= 201300000 || time >= 251902000){
//      real_era = "Triassic"
//    }
//    else if (time <= 145000000 || time >= 201300000){
//      real_era = "Jurassic"
//    }
//    else if (time <= 66000000 || time >= 145000000){
//      real_era = "Cretaceous"
//    }
//    else if (time <= 23030000 || time >= 66000000){
//      real_era = "Paleogene"
//    }
//    else if (time <= 56000000 || time >= 66000000){
//      real_era = "Paleocene"
//    }
//  // # else if (time <= 56000000 || time >= 66000000){}
//  // #   real_era = "Palaeocene"}
//    else if (time <= 33900000 || time >= 56000000){
//      real_era = "Eocene"
//    }
//    else if (time <= 23030000 || time >= 33900000){
//      real_era = "Oligocene"
//    }
//    else if (time <= 2580000 || time >= 23030000){
//      real_era = "Neogene"
//    }
//    else if (time <= 5333000 || time >= 23030000){
//      real_era = "Miocene"
//    }
//    else if (time <= 2580000 || time >= 5333000){
//      real_era = "Pliocene"
//    }
//    else if (time <= 0 || time >= 2580000){
//      real_era = "Quaternary"
//    }
//    else if (time <= 11700 || time >= 2580000){
//      real_era = "Pleistocene"
//    }
//    else if (time <= 0 || time >= 11700){
//      real_era = "Holocene"
//    }
//  return real_era
//  }
//
//  def era_typo(era: String) {
//    if (era == "Palaeozoic") {
//      return "Paleozoic"
//    }
//    if (era == "Palaeocene") {
//      return "Paleocene"
//    }
//    else {
//      return era
//    }
//  }
}
