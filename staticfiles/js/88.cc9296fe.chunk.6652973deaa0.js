(this["webpackJsonperp-frontend"]=this["webpackJsonperp-frontend"]||[]).push([[88],{181:function(e,t,a){"use strict";a.r(t);var n=a(1),r=a(15),c=a.n(r),u=a(28),i=a(47),l=a(0),o=a.n(l),s=a(292),p=a(260),d=a(309),m=a(302),f=a(105),v=a(2),h=a(282),b=a.n(h),g=a(259),y=a(258),E=a(25),O=a(545),j=a(344);t.default=e=>{var t=o.a.useState(!0),a=Object(i.a)(t,2),r=a[0],l=a[1],h=o.a.useState(!1),x=Object(i.a)(h,2),C=x[0],w=x[1],k=o.a.useState([]),L=Object(i.a)(k,2),S=L[0],P=L[1],_=o.a.useState({name:"",category:"",type:"",rate:"",code:"",hasUniqueCode:!1,isLimited:!1,countLimit:"",isActive:!0}),T=Object(i.a)(_,2),G=T[0],q=T[1],N=o.a.useState({}),U=Object(i.a)(N,2),A=U[0],F=U[1];o.a.useEffect(()=>{var t=new AbortController;return Object(u.a)(c.a.mark((function a(){var n;return c.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return n=0,a.next=3,Object(j.g)({action:"get",filter:"none",start:0,end:999999},t.signal).then(e=>{console.log(e),e.json.status&&(P([...e.json.gift_card_categories]),n++)}).catch(e=>{console.log(e)});case 3:return a.next=5,Object(j.f)({action:"get",uuid:e.match.params.id,filter:"uuid"},t.signal).then(function(){var e=Object(u.a)(c.a.mark((function e(t){var a;return c.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(console.log(t.json),!t.json.status){e.next=6;break}return a=t.json.gift_cards[0],e.next=5,q({id:a.id,uuid:a.uuid,name:a.name,category:a.category,type:a.discount_type,rate:a.rate,code:a.code,hasUniqueCode:a.has_unique_codes,isLimited:a.is_limited,countLimit:a.count_limit,isActive:a.is_active});case 5:n++;case 6:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()).catch(e=>{console.log(e)});case 5:2===n&&l(!1);case 6:case"end":return a.stop()}}),a)})))(),()=>t.abort()},[]);var I=e=>{var t;console.log("chainge hte ghints",e.target.value),t=e.target.name,F(Object(n.a)(Object(n.a)({},A),{},{[t]:""}));var a=G;"checkbox"===e.target.type?(console.log("htis is checkobs ------------------"),a[e.target.name]=!a[e.target.name],!0===a.hasUniqueCode&&(a.isLimited=!0)):(console.log("htis is not not ------------------"),a[e.target.name]=e.target.value),q(Object(n.a)({},a))};return r?o.a.createElement(g.a,null):o.a.createElement(v.a,null,o.a.createElement(s.a,null,o.a.createElement(p.a,null,o.a.createElement(d.a,null,o.a.createElement(d.a.Body,null,o.a.createElement("h5",null,"Create Gift Card"),o.a.createElement("hr",null),o.a.createElement(s.a,null,o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Gift Card Name*"),o.a.createElement(m.a.Control,{name:"name",value:G.name,onChange:I,type:"text",placeholder:"Tax Name"}),o.a.createElement(y.a,null,A.name))),o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Gift Card Category"),o.a.createElement(m.a.Control,{name:"category",value:G.category,onChange:I,as:"select"},o.a.createElement("option",{value:"",disabled:!0},"Select..."),S.map((e,t)=>o.a.createElement("option",{key:t,value:e.id},e.name))),o.a.createElement(y.a,null,A.category))),o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Discount Type*"),o.a.createElement(m.a.Control,{name:"type",value:G.type,onChange:I,as:"select"},o.a.createElement("option",{value:"",disabled:!0},"Select..."),o.a.createElement("option",{value:"percent"},"Percent"),o.a.createElement("option",{value:"fixed"},"Fixed")),o.a.createElement(y.a,null,A.type))),o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Rate*"),o.a.createElement(m.a.Control,{name:"rate",value:G.rate,onChange:I,type:"number",placeholder:"Rate"}),o.a.createElement(y.a,null,A.rate))),o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Code*"),o.a.createElement(m.a.Control,{name:"code",value:G.code,onChange:I,type:"text",placeholder:"Code"}),o.a.createElement(y.a,null,A.code))),o.a.createElement(p.a,{md:3},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null),o.a.createElement(m.a.Check,{name:"hasUniqueCode",onChange:I,checked:G.hasUniqueCode,style:{padding:"5px",paddingLeft:"20px"},type:"checkbox",label:"Has Unique Code"}),o.a.createElement(y.a,null,A.hasUniqueCode))),o.a.createElement(p.a,{md:3},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null),o.a.createElement(m.a.Check,{name:"isLimited",onChange:I,checked:G.isLimited,style:{padding:"5px",paddingLeft:"20px"},type:"checkbox",label:"Is Limited"}),o.a.createElement(y.a,null,A.isLimited))),G.isLimited?o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,null,o.a.createElement(m.a.Label,null,"Count Limit*"),o.a.createElement(m.a.Control,{name:"countLimit",value:G.countLimit,onChange:I,type:"number",placeholder:"Count Limit"}),o.a.createElement(y.a,null,A.countLimit))):null,o.a.createElement(p.a,{md:6},o.a.createElement(m.a.Group,{className:"d-flex flex-column justify-content-end"},o.a.createElement(m.a.Label,{style:{marginBottom:"15px"}},"Is Active?"),o.a.createElement(b.a,{onChange:e=>{q(Object(n.a)(Object(n.a)({},G),{},{isActive:e}))},checked:G.isActive})))),o.a.createElement("div",{className:"d-flex justify-content-end"},o.a.createElement(f.a,{variant:"warning",onClick:()=>{e.history.push("/gift-cards")}},"Cancel"),o.a.createElement(f.a,{disabled:C,variant:"primary",onClick:()=>{var t=Object(O.a)(G),a=t.isValid,r=t.errors;if(!a)return console.log(r),void F(Object(n.a)({},r));console.log("no errros"),w(!0);var c={action:"update",gift_card_uuid:G.uuid,name:G.name,code:G.code,discount_type:G.type,rate:parseFloat(G.rate),is_limited:G.isLimited,has_unique_codes:G.hasUniqueCode,count_limit:parseInt(G.countLimit),category:parseInt(G.category),is_active:G.isActive};console.log(JSON.stringify(c)),Object(j.l)(c).then(t=>{t.json.status?(E.a.fire({icon:"success",title:"Gift Card updated successfully!",background:"#dffff0"}),e.history.push("/gift-card/"+G.uuid)):(w(!1),E.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"}))}).catch(e=>{w(!1),console.log(e)})}},C?o.a.createElement(o.a.Fragment,null,o.a.createElement("i",{className:"fa fa-spinner text-c-white f-15 fa-pulse m-l-1"}),"Updating"):"Update")))))))}},258:function(e,t,a){"use strict";var n=a(0),r=a.n(n),c=a(302),u=a(31);t.a=e=>Object(u.a)(e.children)?r.a.createElement("span",null):r.a.createElement(r.a.Fragment,null,r.a.createElement(c.a.Text,{style:{color:"red"}},e.children))},259:function(e,t,a){"use strict";var n=a(0),r=a.n(n);t.a=()=>r.a.createElement("div",{className:"loader-bg"},r.a.createElement("div",{className:"loader-track"},r.a.createElement("div",{className:"loader-fill"})))},344:function(e,t,a){"use strict";a.d(t,"b",(function(){return i})),a.d(t,"g",(function(){return l})),a.d(t,"h",(function(){return o})),a.d(t,"m",(function(){return s})),a.d(t,"c",(function(){return p})),a.d(t,"a",(function(){return f})),a.d(t,"i",(function(){return d})),a.d(t,"f",(function(){return m})),a.d(t,"l",(function(){return v})),a.d(t,"d",(function(){return h})),a.d(t,"e",(function(){return b})),a.d(t,"k",(function(){return g})),a.d(t,"j",(function(){return y}));var n=a(15),r=a.n(n),c=a(28),u=a(41),i=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/category/add","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/categories/get","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),o=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/category/get","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),s=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/category/update","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/category/delete","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),d=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/get","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),m=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/get","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),f=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/add","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),v=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/update","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),h=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcards/delete","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),b=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/uniquecard/delete","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),g=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/redeem","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}(),y=function(){var e=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/payment/giftcard/redeem/history","POST",t,a);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,a){return e.apply(this,arguments)}}()},545:function(e,t,a){"use strict";a.d(t,"a",(function(){return r}));var n=a(31),r=e=>{var t={};return Object(n.a)(e.name)&&(t.name="Name of tax cannot be empty!"),Object(n.a)(e.type)&&(t.type="Provide discount type of gift card!"),Object(n.a)(e.rate)&&(t.rate="Provide rate of gift card!"),Object(n.a)(e.code)&&(t.code="Provide code of gift card!"),e.isLimited&&Object(n.a)(e.countLimit)&&(t.countLimit="Provide count limit of gift card!"),{isValid:Object(n.a)(t),errors:t}}}}]);
//# sourceMappingURL=88.cc9296fe.chunk.js.map