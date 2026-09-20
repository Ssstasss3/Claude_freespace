import { reportCorrelation } from './guarded_stats.mjs';
/* span is (max-min)/|median|. When the median sits at ~0 the guard sets span to
   Infinity and always reports. A variable centred on zero therefore passes the
   manipulation check no matter how little it moved. */
console.log(reportCorrelation({
  label:'variable centred on zero, moves 0.02 total',
  variable:[-0.01, 0.00, 0.00, 0.01], outcome:[8,3,9,2], unit:''
}).text);
console.log();
console.log(reportCorrelation({
  label:'same tiny movement, shifted off zero (median 5.00)',
  variable:[4.99, 5.00, 5.00, 5.01], outcome:[8,3,9,2], unit:''
}).text);
