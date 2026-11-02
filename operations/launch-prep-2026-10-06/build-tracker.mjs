import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out='F:/Dropshipping/outputs/01a10c16-2853-7d31-beb1-8ba2ec9f15d6';
const wb=Workbook.create(),results=wb.worksheets.add('Results'),cohorts=wb.worksheets.add('Cohorts');
for(const s of [results,cohorts]){s.showGridLines=false;s.getRange('A1:N70').format.font={name:'Arial',size:11,color:'#26342E'};s.getRange('A1:N70').format.rowHeight=25;s.getRange('A1:N70').format.verticalAlignment='center';}
results.getRange('A2').values=[['Rozmiso sales results']];results.getRange('A2').format.font={size:16,bold:true};
results.getRange('A4:B4').values=[['Metric','Closed cohorts only']];
results.getRange('A5:A13').values=[['Closed cohorts'],['Ad spend (INR)'],['Placed orders'],['Retained delivered orders'],['Net revenue (INR)'],['Contribution after ads (INR)'],['Ad cost / placed order (INR)'],['Ad cost / retained order (INR)'],['Contribution / net revenue']];
results.getRange('B5').formulas=[['=COUNTIFS(\'Cohorts\'!$N$8:$N$67,"Closed",\'Cohorts\'!$M$8:$M$67,"Complete")']];
for(const [r,c] of [[6,'C'],[7,'E'],[8,'F'],[9,'G'],[10,'L']])results.getRange('B'+r).formulas=[[`=IF(B5=0,"",SUMIFS('Cohorts'!$${c}$8:$${c}$67,'Cohorts'!$N$8:$N$67,"Closed",'Cohorts'!$M$8:$M$67,"Complete"))`]];
results.getRange('B11:B13').formulas=[['=IF(OR(B5=0,B7=0),"",B6/B7)'],['=IF(OR(B5=0,B8=0),"",B6/B8)'],['=IF(OR(B5=0,B9=0),"",B10/B9)']];
results.getRange('A16:B17').values=[['Pending cohorts',null],['Closed cohorts missing inputs',null]];
results.getRange('B16').formulas=[['=COUNTIFS(\'Cohorts\'!$N$8:$N$67,"Pending")']];results.getRange('B17').formulas=[['=COUNTIFS(\'Cohorts\'!$N$8:$N$67,"Closed",\'Cohorts\'!$M$8:$M$67,"Missing inputs")']];
results.getRange('A20').values=[['Start by entering one order-date cohort on the Cohorts sheet.']];results.getRange('A21').values=[['Close a cohort after delivery, returns and settlements are reconciled.']];results.getRange('A22').values=[['Blank results mean there is no complete, closed cohort yet.']];
results.getRange('A24').values=[['Contribution includes allocated operating costs, before income tax.']];
results.getRange('A:A').format.columnWidth=45;results.getRange('B:B').format.columnWidth=25;results.getRange('C:C').format.columnWidth=40;
results.getRange('B6:B12').setNumberFormat('"₹"#,##0.00;("₹"#,##0.00);"₹"0.00');results.getRange('B7:B8').setNumberFormat('#,##0');results.getRange('B13').setNumberFormat('0.0%');
cohorts.getRange('A2').values=[['Order-date cohorts']];cohorts.getRange('A2').format.font={size:16,bold:true};
cohorts.getRange('A3').values=[['Enter actuals from Shopify, supplier invoices, courier settlements and your advertising account.']];
cohorts.getRange('A4').values=[['One row covers orders placed on that date for the selected product or campaign. Keep costs and orders in the same cohort.']];
cohorts.getRange('A5').values=[['Net revenue: collected revenue after refunds, excluding output GST. Product costs: net of recovered stock and eligible tax credits.']];
cohorts.getRange('A6').values=[['Other costs include payment/Shopify fees, packaging, handling and allocated subscription/operating costs. Enter 0 when truly zero.']];
cohorts.getRange('A7:N7').values=[['Order date','Product / campaign','Ad spend (INR)','Sessions','Placed orders','Retained orders','Net revenue (INR)','Net product cost','Freight incl. RTO','Other costs','CAC / placed','Contribution','Input status','Settlement status']];
cohorts.getRange('A8:J67').format.fill='#FFF3D6';cohorts.getRange('N8:N67').format.fill='#FFF3D6';
for(let r=8;r<=67;r++){
cohorts.getRange('M'+r).formulas=[[`=IF(A${r}="","",IF(OR(B${r}="",COUNT(C${r}:J${r})<8,N${r}=""),"Missing inputs","Complete"))`]];
cohorts.getRange('K'+r).formulas=[[`=IF(OR(M${r}<>"Complete",E${r}=0),"",C${r}/E${r})`]];
cohorts.getRange('L'+r).formulas=[[`=IF(M${r}<>"Complete","",G${r}-SUM(H${r}:J${r})-C${r})`]];
}
cohorts.getRange('N8:N67').dataValidation={rule:{type:'list',values:['Pending','Closed']}};
cohorts.getRange('C8:J67').dataValidation={rule:{type:'decimal',operator:'greaterThanOrEqual',formula1:0}};
cohorts.getRange('D8:F67').dataValidation={rule:{type:'whole',operator:'greaterThanOrEqual',formula1:0}};
cohorts.getRange('A8:A67').setNumberFormat('dd-mmm-yy');cohorts.getRange('C8:L67').setNumberFormat('#,##0.00;(#,##0.00);0.00');cohorts.getRange('D8:F67').setNumberFormat('#,##0');
cohorts.getRange('A:A').format.columnWidth=16;cohorts.getRange('B:B').format.columnWidth=30;cohorts.getRange('C:L').format.columnWidth=19;cohorts.getRange('M:N').format.columnWidth=22;
cohorts.getRange('A7:N7').format.wrapText=true;cohorts.getRange('A7:N7').format.rowHeight=48;cohorts.freezePanes.freezeRows(7);cohorts.freezePanes.freezeColumns(2);
for(const [s,r]of[[results,'A4:B4'],[cohorts,'A7:N7']])s.getRange(r).format={fill:'#26342E',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true};
cohorts.getRange('L8:L67').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FBE4DE',font:{color:'#8B3020'}}});cohorts.getRange('M8:M67').conditionalFormats.add('containsText',{text:'Missing inputs',format:{fill:'#FBE4DE',font:{color:'#8B3020'}}});
// Authoring-only reconciliation: closed, pending and incomplete cohorts.
cohorts.getRange('A8:J10').values=[[new Date('2026-10-06T00:00:00Z'),'TEST ONLY',100,50,5,4,1000,200,100,50],[new Date('2026-10-07T00:00:00Z'),'TEST ONLY',200,20,2,1,500,100,50,20],[new Date('2026-10-08T00:00:00Z'),'TEST ONLY',null,20,2,1,500,100,50,20]];
cohorts.getRange('N8:N10').values=[['Closed'],['Pending'],['Closed']];wb.recalculate();
if(results.getRange('B10').values[0][0]!==550||results.getRange('B11').values[0][0]!==20||results.getRange('B16').values[0][0]!==1||results.getRange('B17').values[0][0]!==1)throw Error('Tracker reconciliation failed');
cohorts.getRange('A8:J10').clear({applyTo:'contents'});cohorts.getRange('N8:N10').clear({applyTo:'contents'});wb.recalculate();
if(results.getRange('B10').values[0][0]!==''||results.getRange('B5').values[0][0]!==0)throw Error('Blank state failed');
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},summary:'Final formula scan'})).ndjson);
for(const [sheet,range,name]of[['Results','A1:C25','sales-results-preview'],['Cohorts','A1:G12','sales-inputs-preview'],['Cohorts','H7:N12','sales-costs-preview']]){const png=await wb.render({sheetName:sheet,range,scale:1});await fs.writeFile(out+'/'+name+'.png',new Uint8Array(await png.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(out+'/Rozmiso-Sales-Tracker.xlsx');console.log('Tracker exported; synthetic tests removed.');
