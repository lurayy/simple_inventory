(this["webpackJsonperp-frontend"]=this["webpackJsonperp-frontend"]||[]).push([[87],{224:function(e,t,n){"use strict";n.r(t);var a=n(20),r=n.n(a),c=n(1),u=n(33),s=n(55),o=n(0),i=n.n(o),l=n(296),p=n(264),f=n(313),d=n(306),v=n(111),m=n(3),b=n(286),h=n.n(b),O=n(262),j=n(30),x=n(263),E=n(271),y=n(574);t.default=function(e){var t=i.a.useState(!0),n=Object(s.a)(t,2),a=n[0],o=n[1],b=i.a.useState(!1),w=Object(s.a)(b,2),g=w[0],k=w[1],S=i.a.useState({id:"",name:"",type:"",rate:"",code:"",isActive:!1}),P=Object(s.a)(S,2),T=P[0],C=P[1],N=i.a.useState({}),A=Object(s.a)(N,2),_=A[0],D=A[1];i.a.useEffect((function(){var t=new AbortController;return Object(u.a)(r.a.mark((function n(){return r.a.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,Object(E.h)({action:"get",discount_id:e.match.params.id},t.signal).then(function(){var e=Object(u.a)(r.a.mark((function e(t){var n;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(console.log(t),!t.json.status){e.next=9;break}return n=t.json.discounts[0],e.next=5,C(Object(c.a)(Object(c.a)({},T),{},{id:n.id,name:n.name,type:n.discount_type,rate:n.rate,code:n.code,isActive:n.is_active}));case 5:return e.next=7,o(!1);case 7:e.next=10;break;case 9:j.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"});case 10:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()).catch((function(e){console.log(e)}));case 2:case"end":return n.stop()}}),n)})))(),function(){return t.abort()}}),[]);var G=function(e){var t;t=e.target.name,D(Object(c.a)(Object(c.a)({},_),{},{[t]:""})),C(Object(c.a)(Object(c.a)({},T),{},{[e.target.name]:e.target.value}))};return a?i.a.createElement(x.a,null):i.a.createElement(m.a,null,i.a.createElement(l.a,null,i.a.createElement(p.a,null,i.a.createElement(f.a,null,i.a.createElement(f.a.Body,null,i.a.createElement("h5",null,"Update Discount"),i.a.createElement("hr",null),i.a.createElement(l.a,null,i.a.createElement(p.a,{md:6},i.a.createElement(d.a.Group,null,i.a.createElement(d.a.Label,null,"Discount Name*"),i.a.createElement(d.a.Control,{name:"name",value:T.name,onChange:G,type:"text",placeholder:"Discount Name"}),i.a.createElement(O.a,null,_.name))),i.a.createElement(p.a,{md:6},i.a.createElement(d.a.Group,null,i.a.createElement(d.a.Label,null,"Discount Type*"),i.a.createElement(d.a.Control,{name:"type",value:T.type,onChange:G,as:"select"},i.a.createElement("option",{value:"",disabled:!0},"Select..."),i.a.createElement("option",{value:"percent"},"percent"),i.a.createElement("option",{value:"fixed"},"Fixed")),i.a.createElement(O.a,null,_.type))),i.a.createElement(p.a,{md:3},i.a.createElement(d.a.Group,null,i.a.createElement(d.a.Label,null,"Rate*"),i.a.createElement(d.a.Control,{name:"rate",value:T.rate,onChange:G,type:"number",placeholder:"Rate"}),i.a.createElement(O.a,null,_.rate))),i.a.createElement(p.a,{md:3},i.a.createElement(d.a.Group,null,i.a.createElement(d.a.Label,null,"Code"),i.a.createElement(d.a.Control,{name:"code",value:T.code,onChange:G,type:"text",placeholder:"Code"}),i.a.createElement(O.a,null,_.code))),i.a.createElement(p.a,{md:6},i.a.createElement(d.a.Group,{className:"d-flex flex-column justify-content-end"},i.a.createElement(d.a.Label,{style:{marginBottom:"15px"}},"Is Active?"),i.a.createElement(h.a,{onChange:function(e){console.log(e),C(Object(c.a)(Object(c.a)({},T),{},{isActive:e}))},checked:T.isActive})))),i.a.createElement("div",{className:"d-flex justify-content-end"},i.a.createElement(v.a,{variant:"warning",onClick:function(){e.history.push("/discounts")}},"Cancel"),i.a.createElement(v.a,{disabled:g,variant:"primary",onClick:function(){var t=Object(y.a)(T),n=t.isValid,a=t.errors;if(!n)return console.log(a),void D(Object(c.a)({},a));k(!0);var r={action:"update",discount_id:T.id,discount_type:T.type,name:T.name,rate:parseFloat(T.rate),code:T.code,is_active:T.isActive};console.log(r),Object(E.n)(r).then((function(t){t.json.status?(j.a.fire({icon:"success",title:"Discount updated successfully!",background:"#dffff0"}),e.history.push("/discounts")):(k(!1),j.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"}))})).catch((function(e){k(!1),console.log(e)}))}},g?i.a.createElement(i.a.Fragment,null,i.a.createElement("i",{className:"fa fa-spinner text-c-white f-15 fa-pulse m-l-1"}),"Updating"):"Update")))))))}},262:function(e,t,n){"use strict";var a=n(0),r=n.n(a),c=n(306),u=n(36);t.a=function(e){return Object(u.a)(e.children)?r.a.createElement("span",null):r.a.createElement(r.a.Fragment,null,r.a.createElement(c.a.Text,{style:{color:"red"}},e.children))}},263:function(e,t,n){"use strict";var a=n(0),r=n.n(a);t.a=function(){return r.a.createElement("div",{className:"loader-bg"},r.a.createElement("div",{className:"loader-track"},r.a.createElement("div",{className:"loader-fill"})))}},271:function(e,t,n){"use strict";n.d(t,"j",(function(){return O})),n.d(t,"b",(function(){return j})),n.d(t,"o",(function(){return E})),n.d(t,"e",(function(){return x})),n.d(t,"k",(function(){return h})),n.d(t,"i",(function(){return s})),n.d(t,"a",(function(){return i})),n.d(t,"d",(function(){return o})),n.d(t,"n",(function(){return p})),n.d(t,"h",(function(){return l})),n.d(t,"m",(function(){return f})),n.d(t,"c",(function(){return v})),n.d(t,"f",(function(){return d})),n.d(t,"p",(function(){return b})),n.d(t,"l",(function(){return m})),n.d(t,"g",(function(){return y}));var a=n(20),r=n.n(a),c=n(33),u=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/discounts/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),o=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/discounts/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/discount/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/discount/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/discount/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),f=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/taxes/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),d=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/taxes/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),v=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/tax/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),m=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/tax/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),b=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/sales/tax/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),h=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/inventory/purchaseorders/status","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),O=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/inventory/placements/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),j=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),x=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),E=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),y=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(u.a)("api/v1/user/countries/get ","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},574:function(e,t,n){"use strict";n.d(t,"a",(function(){return r}));var a=n(36),r=function(e){var t={};return Object(a.a)(e.name)&&(t.name="Provide name of discount!"),Object(a.a)(e.type)&&(t.type="Provide type of discount!"),Object(a.a)(e.rate)&&(t.rate="Provide rate of discount!"),{isValid:Object(a.a)(t),errors:t}}}}]);
//# sourceMappingURL=87.3abd1aa2.chunk.js.map