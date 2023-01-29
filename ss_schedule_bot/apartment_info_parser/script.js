(async () => {
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        };

        await agent.goto('https://ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-2-%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D0%BD%D0%B0%D1%8F-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0--6195952');

        await agent.waitForState({
            name: 'dlfLoaded',
            all(assert) {
                assert(agent.isPaintingStable);
            },
        });
        await sleep(200)
        const modalDialog = await agent.querySelector("#WarningPopUp > div > div > div.modal-footer > a")
        if (modalDialog) {
            await modalDialog.$click()

        }

        let selector = await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div > div.author_contact_info > div.UserMObileNumbersBlock > div')
        while (!selector) {
            await sleep(50)
            selector = await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div > div.author_contact_info > div.UserMObileNumbersBlock > div')

        }
        let number = await selector.textContent
        while (number.includes("*")) {
            await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div.mobile-phone-row-top > div.author_contact_info').click()
            await sleep(400)
            selector = await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.phone-row--realEstate > div.phone-row-top > div.author_contact_info2 > div.UserMObileNumbersBlock > a > span')
            if (selector) {
                number = await selector.textContent
            }

        }
        resolve(await agent.document.documentElement.innerHTML);

    }
)();