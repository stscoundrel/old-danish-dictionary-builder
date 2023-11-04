package io.github.stscoundrel.scraper

import io.github.stscoundrel.scraper.services.ScraperService
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication


@SpringBootApplication
class ScraperApplication

fun main(args: Array<String>) {
    runApplication<ScraperApplication>(*args)
    val scraper = ScraperService()
    scraper.scrape()
}


