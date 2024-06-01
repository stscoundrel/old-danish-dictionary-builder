package io.github.stscoundrel.analyzer

import java.io.BufferedReader
import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Paths

class Reader {
    private val classLoader = Thread.currentThread().contextClassLoader
    private val resourcePath = "text"
    private val resource = classLoader.getResource(resourcePath)

    private fun listFiles(): List<String> {
        return resource?.toURI()?.let { uri ->
            Files.walk(Paths.get(uri), 1)
                .filter { path -> Files.isRegularFile(path) && path.fileName.toString().endsWith(".txt") }
                .map { path -> path.fileName.toString() }
                .toList()
        } ?: emptyList()
    }

    private fun readFile(fileName: String): List<String> {
        val inputStream = classLoader.getResourceAsStream("$resourcePath/$fileName")
        return inputStream?.bufferedReader(StandardCharsets.UTF_8)?.use(BufferedReader::readLines) ?: emptyList()
    }

    fun readOCRTextFiles(): Map<String, List<String>> {
        return listFiles().associateWith { readFile(it) }
    }
}