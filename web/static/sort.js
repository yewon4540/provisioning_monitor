// function sortTable(n) {
//     console.log("✅ sortTable called on column:", n);

//     const table = document.getElementById("statusTable");
//     let switching = true;
//     let dir = "asc";
//     let switchcount = 0;

//     while (switching) {
//         switching = false;
//         const rows = table.rows;

//         for (let i = 1; i < rows.length - 1; i++) {
//             let shouldSwitch = false;

//             const x = rows[i].getElementsByTagName("TD")[n];
//             const y = rows[i + 1].getElementsByTagName("TD")[n];

//             const xVal = parseCellValue(x.textContent);
//             const yVal = parseCellValue(y.textContent);

//             if ((dir === "asc" && xVal > yVal) || (dir === "desc" && xVal < yVal)) {
//                 rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
//                 switching = true;
//                 switchcount++;
//                 break;
//             }
//         }

//         if (!switching && switchcount === 0 && dir === "asc") {
//             dir = "desc";
//             switching = true;
//         }
//     }
// }

// function parseCellValue(text) {
//     text = text.trim();

//     if (text === "-" || text === "") return -Infinity;

//     // IP 주소: "10.41.0.25"
//     if (/^\d+\.\d+\.\d+\.\d+$/.test(text)) {
//         return text.split('.').map(num => parseInt(num, 10));
//     }

//     // 위치명, 예: "1강의장", "10강의장", "(구)알파카랩" → 숫자 추출, 없으면 0
//     const numMatch = text.match(/\d+/);
//     if (numMatch) {
//         return parseInt(numMatch[0], 10);
//     } else {
//         return 0;
//     }

//     // 응답시간 (ms 포함) 처리
//     const number = parseFloat(text.replace(/[^\d.]/g, ""));
//     if (!isNaN(number)) return number;

//     // 날짜 처리
//     if (text.includes("년") && text.includes("월") && text.includes("일")) {
//         const dateStr = text
//             .replace(/년/g, "-")
//             .replace(/월/g, "-")
//             .replace(/일/g, "")
//             .replace(/시/g, ":")
//             .replace(/분 기준/g, "")
//             .replace(/\s+/g, "");
//         return new Date(dateStr);
//     }

//     // 그 외 문자열은 소문자로 정렬
//     return text.toLowerCase();
// }
