const D={tire:/tire|tyre|rubber/i,glass:/glass|window|windscreen|windshield/i,caliper:/caliper|brake(?![ _-]?light)/i,
rim:/(^|[^a-z])rim|alloy|spoke|hub_?cap|wheel(?![ _-]?(well|arch))/i,interior:/leather|seat|interior|dashboard|alcantara|upholster|cabin/i,body:/body|car_?paint|paint|exterior|coachwork/i};
export const PARTS=['body','rim','caliper','glass','interior','badge'];
export function classify({mesh='',mat='',chain=[]},adapter={}){
const own=`${mesh} ${mat}`,near=`${own} ${chain.slice(0,2).join(' ')}`;
if((adapter.ignore||[]).some(r=>r.test(near)))return null;
for(const c of PARTS)if((adapter[c]||[]).some(r=>r.test(near)))return c;
if(D.tire.test(near))return null;                       
if(D.glass.test(own))return'glass';
if(D.caliper.test(near))return'caliper';
if(D.rim.test(near))return'rim';
if(D.interior.test(own))return'interior';
if(D.body.test(own))return'body';
return null}
