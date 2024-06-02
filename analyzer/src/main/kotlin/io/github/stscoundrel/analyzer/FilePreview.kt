package io.github.stscoundrel.analyzer

import java.io.File

class FilePreview(private val resourceNames: List<String>) {
    private val resourcePath: String = "src/main/resources/text"

    fun openFiles() {
        resourceNames.forEach { filename ->
            val file = File(resourcePath, filename)
            if (file.exists()) {
                openFile(file)
            } else {
                println("File not found: ${file.absolutePath}")
            }
        }
    }

    private fun openFile(file: File) {
        val command = when {
            System.getProperty("os.name").startsWith("Mac") -> listOf("open", file.absolutePath)
            else -> throw UnsupportedOperationException("Unsupported operating system")
        }

        ProcessBuilder(command).start()
    }
}