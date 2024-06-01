import io.github.stscoundrel.analyzer.Analyzer
import io.github.stscoundrel.analyzer.Reader

fun main(args: Array<String>) {
    val reader = Reader()
    val analyzer = Analyzer(reader.readOCRTextFiles())
    val skewedPages = analyzer.listSkewedScans()

    println("Detected possibly skewed pages: ${skewedPages.size}")
    skewedPages.sorted().forEach { println(it) }
}