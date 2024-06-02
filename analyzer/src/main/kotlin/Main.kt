import io.github.stscoundrel.analyzer.Analyzer
import io.github.stscoundrel.analyzer.Reader
import io.github.stscoundrel.analyzer.SkewReason

fun outputSkewReasonAndResults(result: Map.Entry<SkewReason, List<String>>) {
    println("Skew reason: ${result.key}. Count: ${result.value.size} \n")
    result.value.forEach { println(it) }

    println()
    println("###########################")
    println()
}

fun main(args: Array<String>) {
    val reader = Reader()
    val analyzer = Analyzer(reader.readOCRTextFiles())
    val skewedPages = analyzer.listSkewedScans()

    skewedPages.forEach{ outputSkewReasonAndResults(it) }
}