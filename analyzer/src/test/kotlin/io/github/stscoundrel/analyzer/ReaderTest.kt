package io.github.stscoundrel.analyzer

import kotlin.test.BeforeTest
import kotlin.test.Test
import kotlin.test.assertEquals

class ReaderTest {
    private lateinit var reader: Reader

    @BeforeTest
    fun setUp() {
        reader = Reader()
    }

    @Test
    fun readsAllFiles() {
        val files = reader.readOCRTextFiles()
        val expectedPagesCount = 3636

        assertEquals(expectedPagesCount, files.size)
    }

    @Test
    fun filesAreReadSuccessfully() {
        val files = reader.readOCRTextFiles()

        val expectedContentInFile = "kring sig som en krefft. 2 Tim 217 (CP, | 313 (ovf. III. 249bs7= ædhenne ware."
        val contentInFile = files["3564-ædelkorn.txt"]?.get(2)

        // First line of semi random page.
        assertEquals(expectedContentInFile, contentInFile)
    }
}