package io.github.stscoundrel.kotlintemplate

import org.junit.Test
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Assert.assertFalse

class AppTest {

    @Test
    fun testCasesRun() {
        assertTrue(true)
        assertFalse(false)

        assertEquals(dummyMethod(2, 2), 4)
        assertEquals(dummyMethod(3, 4), 7)
    }
}