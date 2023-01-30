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
        await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div.mobile-phone-row-top > div.author_contact_info').click()
        while (true) {
            await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div.mobile-phone-row-top > div.author_contact_info').click();
            await sleep(100);
            tag = await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.mobile-phone-row.mobile-phone-row--realEstate > div.mobile-phone-row-bottom > div:nth-child(2) > div.mobile-phone-row-bottom-item-list > a');
            if (tag) {
                break
            }
            selector = await agent.document.querySelector('#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.phone-row--realEstate > div.phone-row-top > div.author_contact_info2 > div.UserMObileNumbersBlock > a > span');
            if (selector) {
                number = await selector.textContent;
                console.log(number);
                console.log(number.includes("*"));
                if (!number.includes("*")){
                    break;
                }
            }

        }
        resolve(await agent.document.documentElement.innerHTML);

    }
)();