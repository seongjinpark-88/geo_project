name := "geoscience_project"

version := "1.0"

scalaVersion := "2.12.8"

crossScalaVersions := List("2.11.6", "2.11.12", "2.12.8", "2.13.0")

libraryDependencies ++= Seq(
  "org.clulab" %% "geonorm" % "0.9.5",
  "org.json4s" %% "json4s-jackson" % "3.7.0-M1"
)
