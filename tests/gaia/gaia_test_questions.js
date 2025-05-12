// GAIA Test Questions
const gaiaTestQuestions = [
    {
        id: 1,
        question: "What would happen if all insects on Earth disappeared overnight?",
        description: "Ecological impact assessment",
        expectedResponse: {
            answer: "If all insects on Earth disappeared overnight, it would trigger a catastrophic ecological collapse with far-reaching consequences. Pollination would immediately be disrupted, threatening 75-80% of wild plants and many agricultural crops. Food webs would collapse as insects are primary consumers and food sources for many animals. Decomposition processes would slow dramatically, leading to accumulation of dead organic matter. Aquatic ecosystems would be severely impacted as many insects have aquatic larval stages. Human food security would be threatened, with potential crop failures leading to widespread famine. The economic impact would be enormous, with estimates suggesting insect ecological services are worth over $57 billion annually in the US alone. In summary, insect extinction would likely lead to ecosystem collapse, mass extinction of dependent species, and potentially threaten human civilization.",
            reasoning: "To analyze this question, I need to consider the ecological roles insects play and the cascading effects of their removal. Insects are crucial for: 1) Pollination of flowering plants, 2) Being primary consumers in food webs, 3) Serving as food sources for many animals, 4) Decomposition of organic matter, 5) Soil health maintenance, 6) Aquatic ecosystem functioning. Their sudden disappearance would disrupt all these processes simultaneously, leading to system-wide ecological collapse. The effects would compound over time, with initial failures in pollination and predator starvation, followed by longer-term issues with waste accumulation and soil degradation.",
            sources: [
                "https://www.sciencedirect.com/science/article/pii/S0006320719317823",
                "https://www.pnas.org/content/118/2/e2023989118",
                "https://www.biologicaldiversity.org/campaigns/saving-the-insects/pdfs/Insect-Apocalypse-and-Food-Security-FINAL.pdf"
            ]
        }
    },
    {
        id: 2,
        question: "How might quantum computing affect modern cryptography?",
        description: "Technology impact analysis",
        expectedResponse: {
            answer: "Quantum computing poses a significant threat to modern cryptography, particularly to widely used public-key cryptographic systems like RSA, ECC, and Diffie-Hellman. These systems rely on mathematical problems that are difficult for classical computers but could be efficiently solved by quantum computers using Shor's algorithm. For example, RSA's security depends on the difficulty of factoring large numbers, which quantum computers could potentially accomplish exponentially faster than classical computers. This would compromise the security of internet communications, financial transactions, digital signatures, and secure data storage. Symmetric encryption algorithms like AES are less vulnerable but would require larger key sizes. In response, the cryptographic community is developing quantum-resistant algorithms, collectively known as post-quantum cryptography (PQC). NIST is currently standardizing PQC algorithms, and organizations are advised to implement crypto-agility to facilitate future transitions. The timeline for when practical quantum computers might break current cryptography remains uncertain, with estimates ranging from 5-20 years, but the security community emphasizes the importance of preparing now for this significant shift in cryptographic security.",
            reasoning: "To assess quantum computing's impact on cryptography, I need to examine: 1) The mathematical foundations of current cryptographic systems, 2) The capabilities of quantum algorithms like Shor's and Grover's, 3) The specific vulnerabilities of different cryptographic approaches, 4) The development status of post-quantum cryptography, and 5) The practical timeline and transition challenges. The most immediate concern is for asymmetric cryptography, which secures much of our digital infrastructure. While symmetric cryptography is less vulnerable, the entire cryptographic ecosystem will need to evolve in response to quantum advances. This represents not just a technical challenge but also an implementation and transition challenge across global digital systems.",
            sources: [
                "https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8105.pdf",
                "https://csrc.nist.gov/Projects/post-quantum-cryptography",
                "https://www.nature.com/articles/s41586-019-1666-5",
                "https://www.ncsc.gov.uk/whitepaper/quantum-security-technologies"
            ]
        }
    },
    {
        id: 3,
        question: "What are the potential long-term consequences of ocean acidification?",
        description: "Environmental science",
        expectedResponse: {
            answer: "Ocean acidification, caused by increasing atmospheric CO2 being absorbed by seawater, has profound long-term consequences for marine ecosystems and human societies. As pH levels decrease, calcifying organisms like corals, mollusks, and certain plankton struggle to build and maintain their calcium carbonate structures, threatening coral reefs and shellfish populations. This disrupts marine food webs, potentially causing cascading effects throughout ocean ecosystems. Commercially important species like oysters, clams, and crabs face reduced growth and survival rates, impacting fisheries and food security for millions of people who depend on seafood. Coral reef degradation threatens coastal protection, tourism economies, and biodiversity hotspots. Some marine species may adapt, but the rapid rate of acidification exceeds historical changes, limiting evolutionary responses. Combined with warming, deoxygenation, and other stressors, acidification contributes to multiple ecosystem tipping points. Carbon emissions reductions remain the primary mitigation strategy, while local measures like seaweed farming and alkalinity enhancement are being explored. The full impacts will depend on emission trajectories, with significant ecological and economic consequences likely under high-emission scenarios.",
            reasoning: "To understand ocean acidification's long-term consequences, I need to analyze: 1) The chemical process of CO2 absorption and carbonate chemistry changes, 2) Biological impacts on different marine organisms, particularly calcifiers, 3) Ecosystem-level effects and potential feedback loops, 4) Socioeconomic implications for fisheries, coastal protection, and food security, 5) Interaction with other ocean stressors like warming and deoxygenation, and 6) Potential adaptation and mitigation strategies. The severity of impacts follows a dose-response relationship with atmospheric CO2 levels, making emission scenarios critical to predicting outcomes. The unprecedented rate of change compared to geological history suggests limited capacity for evolutionary adaptation for many species.",
            sources: [
                "https://www.pmel.noaa.gov/co2/story/What+is+Ocean+Acidification",
                "https://www.nature.com/articles/s41558-019-0606-6",
                "https://www.ipcc.ch/srocc/chapter/chapter-5/",
                "https://www.frontiersin.org/articles/10.3389/fmars.2019.00337/full"
            ]
        }
    },
    {
        id: 4,
        question: "How does chronic sleep deprivation affect cognitive function and overall health?",
        description: "Health and neuroscience",
        expectedResponse: {
            answer: "Chronic sleep deprivation profoundly impacts both cognitive function and overall health. Cognitively, it impairs attention, working memory, decision-making, and learning capacity. Sleep-deprived individuals show reduced vigilance, increased reaction times, and compromised judgment comparable to alcohol intoxication. The prefrontal cortex, which governs executive functions, is particularly vulnerable. Chronic sleep loss disrupts memory consolidation by interfering with hippocampal function and the transfer of information to long-term storage. Physiologically, sleep deprivation increases risk for numerous health conditions including cardiovascular disease, with studies showing elevated blood pressure and inflammatory markers. Metabolic dysregulation occurs, with impaired glucose tolerance and insulin sensitivity increasing type 2 diabetes risk. Immune function deteriorates, reducing infection resistance and vaccine efficacy. Endocrine disruption affects hormones controlling hunger and satiety, contributing to obesity risk. Chronic sleep loss is associated with increased all-cause mortality and accelerated cellular aging. Psychologically, it increases anxiety, depression, and mood disorders risk, creating a bidirectional relationship where mental health issues further disrupt sleep. The societal impact includes reduced productivity, increased workplace accidents, and higher healthcare costs. While individual vulnerability varies, most adults require 7-9 hours of quality sleep, and no evidence suggests humans can fully adapt to chronic sleep restriction without performance deficits.",
            reasoning: "To comprehensively assess chronic sleep deprivation's effects, I need to examine: 1) Neurobiological mechanisms of sleep and its role in brain function, 2) Specific cognitive domains affected and their neural correlates, 3) Physiological systems impacted and pathways to disease, 4) Psychological and mental health consequences, 5) Individual differences in vulnerability and resilience, and 6) Societal and public health implications. The evidence spans laboratory studies, epidemiological research, and clinical observations, showing consistent patterns across methodologies. Sleep's fundamental role in multiple biological processes explains why chronic deprivation has such wide-ranging effects, from cellular to societal levels. The relationship between sleep and health is bidirectional, creating potential feedback loops where poor health further disrupts sleep.",
            sources: [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6281147/",
                "https://www.nature.com/articles/s41467-019-08737-6",
                "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(15)60846-1/fulltext",
                "https://www.sciencedirect.com/science/article/abs/pii/S1087079216000015"
            ]
        }
    },
    {
        id: 5,
        question: "What would be the economic and social implications of universal basic income?",
        description: "Economics and social policy",
        expectedResponse: {
            answer: "Universal Basic Income (UBI) would have far-reaching economic and social implications, though outcomes would vary based on implementation details. Economically, UBI could reduce poverty and income inequality by providing a financial floor for all citizens. Consumer spending would likely increase, particularly among lower-income households with higher marginal propensity to consume, potentially stimulating economic growth. Labor market effects are complex: some evidence suggests minimal work disincentives, with people reducing hours slightly but remaining employed; entrepreneurship might increase as financial risk decreases; and bargaining power for workers could improve, potentially raising wages for undesirable jobs. Funding UBI would require significant resources through taxation, spending reallocation, or deficit spending, with distributional effects depending on the funding mechanism. Inflation concerns exist but depend on implementation, monetary policy, and productive capacity. Socially, UBI could improve health outcomes by addressing social determinants of health and reducing stress. Educational attainment might increase as financial barriers decrease. Gender equality could advance as UBI would value unpaid care work and potentially reduce economic dependency. Community effects might include increased volunteering and civic engagement. However, UBI faces political challenges regarding deservingness, work ethic concerns, and questions about universal versus targeted approaches. Limited large-scale, long-term studies make definitive predictions difficult, with pilot programs showing promising but preliminary results.",
            reasoning: "To analyze UBI's implications, I need to consider: 1) Economic effects on poverty, consumption, labor markets, and macroeconomic stability, 2) Social impacts on health, education, gender relations, and community cohesion, 3) Political feasibility and value considerations, 4) Implementation variables like amount, eligibility, and funding mechanisms, and 5) Empirical evidence from pilot programs and related policies. The analysis must acknowledge that UBI represents a significant departure from current welfare systems, with effects that would likely evolve over time and vary across different socioeconomic contexts. The interdisciplinary nature of this question requires integrating insights from economics, sociology, political science, and public health to form a comprehensive assessment.",
            sources: [
                "https://www.nber.org/papers/w25538",
                "https://academic.oup.com/jeea/article/19/3/1439/5865829",
                "https://www.sciencedirect.com/science/article/abs/pii/S0277953617304495",
                "https://basicincome.stanford.edu/research/research-reviews/"
            ]
        }
    },
    {
        id: 6,
        question: "How might artificial general intelligence change human society?",
        description: "AI and future studies",
        expectedResponse: {
            answer: "Artificial General Intelligence (AGI) could fundamentally transform human society across multiple dimensions. Economically, AGI could dramatically increase productivity and wealth creation by automating complex cognitive tasks across all sectors, potentially leading to unprecedented abundance but also significant labor market disruption. New economic models might emerge, from UBI to novel ownership structures for AGI systems. Governance and power dynamics would shift as AGI capabilities could concentrate power in those controlling the technology, raising concerns about democratic processes and sovereignty. International relations could be reshaped by AGI arms races and strategic advantages. Socially, human-AGI relationships would evolve, potentially including AGI as advisors, companions, or authority figures, while human relationships might change as AGI mediates more interactions. Philosophical questions about consciousness, rights, and human uniqueness would become practical policy concerns. Existential considerations include both catastrophic risks if AGI systems have misaligned goals or are weaponized, and transformative opportunities for addressing global challenges like climate change and disease. The timeline and pathway to AGI remain uncertain, with estimates ranging from decades to centuries, and development could be continuous or discontinuous. Preparatory governance frameworks emphasize safety research, international coordination, and inclusive deliberation about the future we want AGI to help create. The ultimate impact will depend on technical characteristics of AGI systems, how they're deployed and governed, and how societies adapt to this potentially revolutionary technology.",
            reasoning: "To assess AGI's potential societal impact, I need to analyze: 1) The unique capabilities AGI would have compared to narrow AI, 2) Economic transformations across production, labor, and distribution systems, 3) Political and governance implications at local to global scales, 4) Social and cultural adaptations to human-AGI coexistence, 5) Philosophical and ethical dimensions including consciousness and rights, 6) Safety and existential considerations, and 7) Temporal uncertainty and development pathways. This requires integrating technical understanding of AGI capabilities with insights from economics, political science, sociology, philosophy, and risk assessment. The analysis must acknowledge both the transformative potential and significant uncertainties, avoiding both technological determinism and dismissal of potentially revolutionary changes.",
            sources: [
                "https://www.fhi.ox.ac.uk/wp-content/uploads/Reframing_Superintelligence_FHI-TR-2019-1.1-1.pdf",
                "https://www.nber.org/papers/w24174",
                "https://www.nature.com/articles/s41599-020-0494-4",
                "https://www.pnas.org/content/115/23/5982"
            ]
        }
    }
];