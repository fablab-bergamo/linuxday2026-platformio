import assert from 'node:assert/strict'
import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { resolve, extname } from 'node:path'
import { chromium } from 'playwright-chromium'

// Server statico senza fallback SPA, come GitHub Pages in un sottopercorso.
const prefix = '/linuxday2026-platformio/'
const root = resolve('dist')
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' }
const server = createServer(async (req, res) => {
  const path = new URL(req.url, 'http://localhost').pathname
  const file = resolve(root, path.slice(prefix.length) || 'index.html')
  if (!path.startsWith(prefix) || !file.startsWith(`${root}/`)) {
    res.writeHead(404).end()
    return
  }
  try {
    const data = await readFile(file)
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream' }).end(data)
  }
  catch { res.writeHead(404).end() }
})
await new Promise(r => server.listen(0, '127.0.0.1', r))
const origin = `http://127.0.0.1:${server.address().port}`
const browser = await chromium.launch({ headless: true })
try {
  for (const viewport of [{ width: 390, height: 844 }, { width: 844, height: 390 }, { width: 1280, height: 800 }]) {
    const mobile = viewport.width !== 1280
    const context = await browser.newContext({ viewport, hasTouch: mobile, isMobile: mobile })
    const page = await context.newPage()
    await page.goto(origin + prefix)
    const overview = page.getByTitle('Show slide overview', { exact: true })
    if (mobile) await overview.tap()
    else { await overview.hover(); await overview.click() }
    const card = page.locator('.z-modal .grid > div').nth(4).locator('.slidev-slide-container').first()
    // Il contenitore interno non riceve eventi; selezionare la miniatura esterna.
    const target = page.locator('.z-modal .grid > div').nth(4).locator(':scope > div').first()
    await card.waitFor({ state: 'visible' })
    if (mobile) await target.tap()
    else await target.click()
    await page.waitForURL(`${origin}${prefix}#/5`)
    assert.equal((await page.reload()).status(), 200)
    await page.getByTitle('Show slide overview', { exact: true }).waitFor()
    assert.equal(new URL(page.url()).hash, '#/5')
    console.log(`Navigazione e ricaricamento OK: ${viewport.width}×${viewport.height}`)
    await context.close()
  }
}
finally { await browser.close(); await new Promise(r => server.close(r)) }
