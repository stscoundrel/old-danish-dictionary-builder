package io.github.stscoundrel.scraper.services

import com.microsoft.playwright.Page
import com.microsoft.playwright.Playwright
import java.net.URL
import java.nio.file.Files
import java.nio.file.Paths

class ScraperService {
    private val baseUrl = "https://www.hist.uib.no/kalkar"
    private val letterPages = listOf(
        "a",
        "b",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "k",
        "r",
        "s",
        "t",
        "u",
        "v",
        "y",
        "ae",
        "oe",
        "aa",
        "ae" // Hidden page not in navigation.
    )

    private fun getImageLinks(page: Page): MutableList<Pair<String, String>> {
        val headwordsToImageLinks = mutableListOf<Pair<String, String>>()

        letterPages.forEach {
            println("Reading $it")
            val url = "$baseUrl/html/$it.htm"
            page.navigate(url)
            page.waitForLoadState()

            // Extract image links.
            page.querySelectorAll("a").forEach { link ->
                val linkHref = link.getAttribute("href")
                if (linkHref.endsWith("gif")) {
                    val formattedHref = linkHref.replace("../", "$baseUrl/")
                    headwordsToImageLinks.add(Pair(link.textContent(), formattedHref))
                }
            }
        }

        return headwordsToImageLinks
    }

    private fun downloadImage(fileName: String, imageUrl: String) {
        println("Downloading $fileName")
        val classLoader = Thread.currentThread().contextClassLoader
        val url = URL(imageUrl)
        val imageBytes = url.readBytes()

        val outputPath = Paths.get("src/main/resources/images/$fileName.gif")
        Files.write(outputPath, imageBytes)

        println("Image downloaded and saved: $fileName")
    }

    private fun downloadAllImages(headwordsToImageLinks: MutableList<Pair<String, String>>) {
        headwordsToImageLinks.forEachIndexed { index, (fileName, imageUrl) ->
            downloadImage("$index-$fileName", imageUrl)
        }
    }

    fun scrape() {
        // Initialize Playwright
        val playwright = Playwright.create()
        val browser = playwright.chromium().launch()
        val page = browser.newPage()

        // Fetch all image urls.
        val headwordsToImageLinks = getImageLinks(page)

        // Download each image to resources.
        downloadAllImages(headwordsToImageLinks)

        // Close Playwright
        browser.close()
        playwright.close()
    }
}