(async () => {
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        };

        await agent.goto('%s');

        await agent.waitForState({
            name: 'dlfLoaded',
            all(assert) {
                assert(agent.isPaintingStable);
            },
        });

        const cookieButton = await agent.querySelector('#CookieAgreement > button');

        if (cookieButton) {
            await cookieButton.$click()

        }
        await agent.querySelector('#main_block > div.detail-page > div.statement-author.align-items-center.flex-wrap > button').$click()

        let number = await agent.document.querySelector('#main_block > div.detail-page > div.statement-author.align-items-center.flex-wrap > button > div > var').textContent
        while (number.includes("*")) {
            await agent.querySelector('#main_block > div.detail-page > div.statement-author.align-items-center.flex-wrap > button').$click()
            await sleep(50)
            number = await agent.document.querySelector('#main_block > div.detail-page > div.statement-author.align-items-center.flex-wrap > button > div > var').textContent
        }
        resolve(await agent.document.documentElement.innerHTML);
})();