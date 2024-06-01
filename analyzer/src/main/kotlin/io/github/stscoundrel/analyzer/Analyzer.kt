package io.github.stscoundrel.analyzer

class Analyzer(private val filesAndContents: Map<String, List<String>>) {
    private val falsePositiveSkewedPages: List<String> = listOf(
        "0-abbot.txt",
    )

    private fun pageSeemsSkewed(page: Map.Entry<String, List<String>>): Boolean {
        // Generally, last format with odd leftovers mean page
        // was originally skewed, and line-by-line reading causes
        // artifacts on last line.
        return (page.value.last().length < 10) and !falsePositiveSkewedPages.contains(page.key)
    }

    fun listSkewedScans(): List<String> {
        return filesAndContents.filter { pageSeemsSkewed(it) }.map { it.key }
    }
}