package io.github.stscoundrel.analyzer

enum class SkewReason {
    LAST_LINE, TOO_FEW_COLUMNS, TOO_MANY_EMPTY_LINES
}

class Analyzer(private val filesAndContents: Map<String, List<String>>) {
    private val falsePositiveSkewedPagesByLastLine: List<String> = listOf(
        "0-abbot.txt",
    )

    // Ideal page could have up to 55. This will probably need tweaking with time.
    private val thresholdOfColumnMarkers = 30

    private fun pageHasSkewedLikeLastLine(page: Map.Entry<String, List<String>>): Boolean {
        // Generally, last line with odd leftovers mean page
        // was originally skewed, and line-by-line reading causes
        // artifacts on last line.
        return (page.value.last().length < 10) and !falsePositiveSkewedPagesByLastLine.contains(page.key)
    }

    private fun pageHasUnExpectedColumnMarkerCount(page: Map.Entry<String, List<String>>): Boolean {
        // Generally, pages have similar amount of lines, which means similar amount of
        // vertical lines separating columns. Having far fewer than expected points
        // towards a skewed scan / OCRd result.
        return page.value.count { it.contains(" | ") } < thresholdOfColumnMarkers
    }

    private fun pageSeemsSkewed(page: Map.Entry<String, List<String>>): Boolean {
        return pageHasSkewedLikeLastLine(page) or pageHasUnExpectedColumnMarkerCount(page)
    }

    fun listSkewedScans(): Map<SkewReason, List<String>> {
        return mapOf(
            SkewReason.LAST_LINE to filesAndContents.filter { pageHasSkewedLikeLastLine(it) }.map { it.key },
            SkewReason.TOO_FEW_COLUMNS to filesAndContents.filter { pageHasUnExpectedColumnMarkerCount(it) }
                .map { it.key },
        )
    }
}