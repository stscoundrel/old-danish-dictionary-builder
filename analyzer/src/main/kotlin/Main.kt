import io.github.stscoundrel.analyzer.Analyzer
import io.github.stscoundrel.analyzer.Reader

fun main(args: Array<String>) {
    val reader = Reader()
    val analyzer = Analyzer(reader.readOCRTextFiles())

    analyzer.listSkewedScans().sorted().forEach { println(it) }
}