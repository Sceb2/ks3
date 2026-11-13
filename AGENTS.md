# KS3 Exam Bank: project guidance and review

This file records the current design direction and open decisions for the KS3 Exam Bank. It is a proposal for review, not authority to publish content, change Google Sites, or assume ownership of resources. Keep Year 9 in the existing GCSE section unless the project owner requests otherwise.

## Purpose and structure

- Provide one KS3 entry point that can be embedded once in Google Sites. Its own navigation should let pupils move between Year 7, Year 8, tests, topics, resources and Smart Banks, with a clear route back.
- The agreed navigation is year → test → topic. Do not add a direct topic index: different test windows cover different parts of the same topic.
- The existing site organises both years into Tests 1–5. Topics recur in later tests as revision; maintain a single canonical topic/resource entry and associate it with multiple tests, preserving test-specific checklists and scope.
- A single repository may contain multiple HTML pages or views, shared CSS/JavaScript, resource metadata and permitted assets. Choose the implementation after testing navigation within Google Sites; a single embed does not require one enormous HTML file.
- Keep external resources recognisable and verify links and permissions before replacing existing ones. Provide stable routes and plan redirects or a transition for existing Google Sites links.

## Visual and editorial reference

The supplied **Y7 Test 1 Page Updated.html** is the test-page reference. It uses a white paper-like card, dark green (`#07583e`), pale mint (`#e9f4ef`), subdued borders, Arial, generous spacing, rounded tiles and restrained topic accents. It has responsive layouts, light/dark mode, a visible focus state, skip link, reduced-motion and print rules.

Use its direct, encouraging British English and short action-led instructions. Its revision sequence is **Check → Learn → Recall → Practise → Review**. Feature Smart Bank prominently; organise resources by checklist, exam-style questions and answers, knowledge organisers, multiple-choice quizzes and other useful sites. Give concise purpose and estimated time where appropriate. Topic sections expand and collapse. Identify external destinations and announce new tabs to screen readers.

The supplied **Smart Bank Heat Transfers.HTML** is the available Smart Bank reference. It uses the same green/mint visual family, a numbered topic navigation, learning objectives, short illustrated learning slides, key ideas, quick checks with explanatory feedback, optional videos and thinking prompts, followed by assessments. Task types include multiple choice, matching via dropdowns and numeric responses; its code also supports multiple select. It includes flashcards, a learning checklist with red/amber/green and not-tried states, reset confirmation, and image credits. Checked assessments inform the checklist; quick checks do not. Progress lasts only while the page is open. Preserve these distinctions and meaningful feedback when adapting it. The owner wants these features across Smart Banks, with a variable number of learning pages suited to each topic. Provide selectable dark mode throughout the experience; the reference Smart Bank currently only has a light design.

The supplied **Smart Bank Diffusion.htm** is a saved OneDrive webpage, not the interactive Smart Bank source. It cannot be used to review the Diffusion learning tasks or to reconstruct that bank. Obtain the actual HTML before comparing or migrating it.

## Existing resource audit (9 November 2026)

The public navigation has Year 7 and Year 8 test pages. The Year 7 Test 1 page is a custom embed: its resource links were not extractable from the static site response, so the supplied updated HTML was reviewed separately. The other nine test pages were inspected from their public HTML. Counts below are distinct labelled links per page, not unique files across the site; repeated resources and different sharing URLs may refer to the same item. File and folder classifications use the SharePoint link format and have not been confirmed by inspecting the documents.

| Test page | SharePoint file links | SharePoint folder links | Microsoft Forms links |
| --- | ---: | ---: | ---: |
| Y7 Test 1 | Embedded; use supplied source | Embedded | Embedded |
| Y7 Test 2 | 8 | 2 | 13 |
| Y7 Test 3 | 11 | 3 | 15 |
| Y7 Test 4 | 14 | 3 | 21 |
| Y7 Test 5 | 23 | 6 | 35 |
| Y8 Test 1 | 10 | 3 | 15 |
| Y8 Test 2 | 12 | 3 | 19 |
| Y8 Test 3 | 16 | 5 | 23 |
| Y8 Test 4 | 18 | 5 | 27 |
| Y8 Test 5 | 30 | 7 | 35 |

Across those nine pages the scan found 196 distinct URLs in these categories, including Microsoft Forms; this is not a count of unique documents. Resources include whole-term and topic checklists, knowledge organisers such as Cell Structure and Diffusion, and exam-style question folders. Forms provide topic quizzes. The supplied Y7 Test 1 page also links to Bitesize, Oak Academy, YouTube and Seneca.

The scanned test themes are: Y7 Test 2 Cells and Energy; Test 3 Cells revision, Chemicals and Forces; Test 4 Energy revision, Chemicals and Forces; Test 5 Cells, Energy, Chemicals, Forces, Interdependence and Electricity. Y8 Test 1 revises Y7 Cells and covers Human Body and Heating and Cooling; Test 2 revises Y7 Energy alongside Human Body and Heating and Cooling; Test 3 revises Y7 Chemicals, Forces and Heating and Cooling alongside Periodic Table and Staying Alive; Test 4 revises Y7 Electricity, Interdependence and Human Body alongside Periodic Table and Staying Alive; Test 5 covers Y7 Key Points, Human Body, Periodic Table, Heating and Cooling, Staying Alive, Restless Earth and Chemical Reactions. Verify exact topic content against the source pages when building each test.

A sampled SharePoint document and exam-question folder redirected to Microsoft sign-in; their actual contents, ownership, permissions and downloadability remain unverified. A sampled Microsoft Forms link returned an HTML page on forms.cloud.microsoft; quiz operation and access were not verified. Do not interpret a sign-in page as the resource itself.

On a further check, ten sampled SharePoint file links all redirected to Microsoft sign-in. The project owner is happy for copies of checklists and knowledge organisers to be stored in Git. Other document categories, including answers, require separate confirmation.

The owner subsequently supplied checklist and knowledge organiser archives: their 58 PDF checklists and 42 organiser files (32 PDFs, 10 PowerPoint files) are stored under `resources/`. Split Year 7 and Year 8 exam-question archives have also been extracted (308 PDFs and one DOCX). Archive integrity checks passed. `RESOURCE-MAPPING.md` contains provisional filename-based candidates for the test-page document links and the question-pack inventory; source documents behind Microsoft sign-in have not been compared, and test-to-term assumptions, approximate titles and file contents require review.

## Resource strategy

Prefer stable local copies of school-owned or otherwise licensed static resources when permission to redistribute is confirmed. Store one canonical copy and reference it from each relevant test; maintain a resource catalogue with title, type, topic, test associations, original URL, local path, source/rights, version and verification status. Check file size and public-hosting limits before committing large files; consider managed storage for large collections. A public repository or GitHub Pages would make committed files public, so confirm school policy and avoid private student data, restricted mark schemes and sensitive materials.

SharePoint links retained in the repository still depend on the account, sharing permissions and availability. Use them as a temporary bridge where local copies are not yet available and flag them for review. Folder links need a file-level inventory before migration. Do not copy third-party documents or media without appropriate permission; link to the publisher when reuse is unclear. Preserve image licences and attribution.

Microsoft Forms links remain dependent on Microsoft and their existing owner. Keeping a link does not migrate the quiz. Rebuilding a quiz in the app needs its questions, answers, feedback and permission, and requires a decision about whether response collection or teacher reporting must be retained.

The owner confirms existing quizzes are anonymous Forms and teacher reporting is not needed. Preserve working Forms links during migration unless a replacement approach is agreed.

Smart Bank progress may clear when the page is closed. Within the same open session, checked assessment answers must update the RAG learning checklist, and navigation within the bank must preserve that session's progress.

Practice question selection follows **test → topic → difficulty (Developing, Secure, Extending) → available question packs**. Show all available packs in the relevant topic folder at each test window and let students choose; students can use their checklist to identify the material covered in their test. Maintain one canonical copy of each file and reuse it across tests. Levels have differing pack counts. Two sampled PDFs contain their mark schemes within the PDF; do not assume separate answer files or that all packs contain answers. Whole practice papers outside the topic folders need a placement decision. Year 7 Test 5 takes place in Term 6 and uses Term 6 checklists.

## Decisions before implementation

1. Decide the placement of whole practice papers and public availability of answers.
2. Confirm the complete source materials, including working Diffusion and Cell Structure Smart Bank HTML, and whether existing pages should be preserved exactly or edited for consistency.
3. Agree dark-mode colours, typography, topic accents and the preferred mobile layout, and test the selectable theme across pages.
4. Confirm the exact meaning of session continuity across page refreshes or navigation between different embedded pages; closing the page may clear progress.
5. Determine the appropriate number of learning pages and topic-specific content for each Smart Bank, retaining the agreed features.
6. Confirm which static documents can be made public, who owns them, whether exam answers should be public, and who can supply original files and folder inventories. Choose a hosting location and access model.
7. Decide whether to retain Forms, recreate quizzes, or do both; identify any need for teacher reporting and student accounts.
8. Agree how Google Sites embed height, scrolling, internal links, browser back, direct links to topics and accessibility will work. Test a representative prototype on desktop and mobile before migrating all pages.
9. Decide the migration order, content owner, accuracy review and process for keeping shared resources current. Verify links, accessibility, interactive tasks and source attribution before publication.

## Year 7 development branch redesign (13 November 2026)

The `development` branch now contains the approved Year 7 Test 1 visual direction across `index.html` and `year-7-test-1.html` through `year-7-test-5.html`. The year hub links to each test; each test links to its own topic views. The current checklist illustration is `assets/checklist-three-arrows.png`. Do not treat the untracked earlier image experiments or preview ZIP as site assets.

`data/year7-resources.json` is the link inventory taken from the pre-redesign Year 7 pages. `scripts/extract-year7.py` reproduces that inventory from commit `24884d1`; `scripts/build-year7.py` generates the new static pages using the approved draft styles and the inventory. Keep test-specific Forms and checklists in their corresponding test entries. Test 5 uses Term 6 checklists. Retain the full Developing, Secure and Extending question-pack lists for each topic, and link to external revision sites rather than copying their content.

The Test 1 legacy page used SharePoint checklist links. The new version uses the matching local Term 1 PDFs from the supplied resources. The two already-existing Smart Banks remain linked on Test 1. No additional Smart Bank pages have been created. Check the public GitHub Pages result and Google Sites embedding before promoting `development` to `main`.

## Year 7 interactive PLC checklists

All five Year 7 tests and their topic views use an in-page PLC dialog. The 22 linked source PDFs (five whole-test and 17 topic checklists) are mapped in `data/year7-plc.json`, generated by `scripts/extract-year7-plc.py`. Term 6 sources are used for Test 5. The original PDF remains available through a secondary link inside each dialog. R/A/G selections are stored per test and checklist in `sessionStorage` for the current browser tab. `assets/plc.js` and `assets/plc.css` provide the interactive window; a locally vendored MIT-licensed jsPDF build creates the filled PDF in a new tab. This does not create teacher reporting or a server-side student record. Keep source PDFs and generated PLC outcomes aligned when editing any checklist.
