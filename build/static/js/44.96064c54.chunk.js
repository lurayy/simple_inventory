(this["webpackJsonperp-frontend"]=this["webpackJsonperp-frontend"]||[]).push([[44],{175:function(e,t,n){"use strict";n.r(t);var a=n(1),r=n(2),c=n(55),o=n(0),s=n.n(o),u=n(296),i=n(264),l=n(313),p=n(306),h=n(111),f=(n(286),n(3)),d=n(276),m=n(451),v=(n(283),n(262)),b=n(30),y=n(431),O=n(263),j=n(311),x=n(271),w=n(36);t.default=function(e){var t=s.a.useState(!0),n=Object(c.a)(t,2),o=n[0],g=n[1],E=s.a.useState([]),k=Object(c.a)(E,2),S=k[0],C=k[1],T=s.a.useState(!1),P=Object(c.a)(T,2),N=P[0],M=P[1],L=s.a.useState({fname:"",lname:"",mname:"",category:"",email:"",website:"",tax:"",phone1:"",phone2:"",address:"",country:"",countryName:""}),D=Object(c.a)(L,2),R=D[0],G=D[1],I=s.a.useState([]),H=Object(c.a)(I,2),_=H[0],z=H[1],A=s.a.useState({}),B=Object(c.a)(A,2),W=B[0],F=B[1];s.a.useEffect((function(){var e=new AbortController;return Object(y.c)({action:"get",filter:"none",start:0,end:999999},e.signal).then((function(e){console.log(e),e.json.status?(C(Object(r.a)(e.json.customerCategories)),g(!1)):b.a.fire({icon:"error",title:e.json.error,background:"#ffe5de"})})).catch((function(e){console.log(e)})),Object(x.g)({action:"get"},e.signal).then((function(e){console.log(e),e.json.status&&z(Object(r.a)(e.json.countries.map((function(e){return{label:e.name,value:e.id}}))))})).catch((function(e){console.log(e)})),function(){return e.abort()}}),[]);var U=function(e){console.log("chaing",e.target.value),F(Object(a.a)(Object(a.a)({},W),{},{[e.target.name]:""})),G(Object(a.a)(Object(a.a)({},R),{},{[e.target.name]:e.target.value}))};return console.log(R),o?s.a.createElement(O.a,null):s.a.createElement(f.a,null,s.a.createElement(u.a,null,s.a.createElement(i.a,null,s.a.createElement(l.a,null,s.a.createElement(l.a.Body,null,s.a.createElement("h5",null,"Create Customer"),s.a.createElement("hr",null),s.a.createElement(u.a,null,s.a.createElement(i.a,{md:4},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"First Name*"),s.a.createElement(p.a.Control,{name:"fname",value:R.fname,onChange:U,type:"text",placeholder:"First Name"}),s.a.createElement(v.a,null,W.fname))),s.a.createElement(i.a,{md:4},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Middle Name"),s.a.createElement(p.a.Control,{name:"mname",value:R.mname,onChange:U,type:"text",placeholder:"Middle Name"}),s.a.createElement(v.a,null,W.mname))),s.a.createElement(i.a,{md:4},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Last Name*"),s.a.createElement(p.a.Control,{name:"lname",value:R.lname,onChange:U,type:"text",placeholder:"Last Name"}),s.a.createElement(v.a,null,W.lname))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Customer Category"),s.a.createElement(p.a.Control,{name:"category",value:R.category,onChange:U,as:"select"},s.a.createElement("option",{value:"",disabled:!0},"Select Customer Category"),S.map((function(e,t){return s.a.createElement("option",{key:t,value:e.id},e.name)}))),s.a.createElement(v.a,null,W.category))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Email*"),s.a.createElement(p.a.Control,{name:"email",value:R.email,onChange:U,type:"email",placeholder:"Email"}),s.a.createElement(v.a,null,W.email))),s.a.createElement(i.a,{md:12},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Address"),s.a.createElement(p.a.Control,{name:"address",value:R.address,onChange:U,type:"text",placeholder:"Address"}),s.a.createElement(v.a,null,W.address))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Phone No 1*"),s.a.createElement(p.a.Control,{name:"phone1",value:R.phone1,onChange:U,type:"tel",placeholder:"Phone No 1"}),s.a.createElement(v.a,null,W.phone1))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Phone No 2"),s.a.createElement(p.a.Control,{name:"phone2",value:R.phone2,onChange:U,type:"tel",placeholder:"Phone No 2"}),s.a.createElement(v.a,null,W.phone2))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Tax Number"),s.a.createElement(p.a.Control,{name:"tax",value:R.tax,onChange:U,type:"number",placeholder:"Tax Number"}),s.a.createElement(v.a,null,W.tax))),s.a.createElement(i.a,null,s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Website"),s.a.createElement(p.a.Control,{name:"website",value:R.website,onChange:U,type:"text",placeholder:"Website"}),s.a.createElement(v.a,null,W.website))),s.a.createElement(i.a,{md:6},s.a.createElement(p.a.Group,null,s.a.createElement(p.a.Label,null,"Country"),s.a.createElement(d.a,{value:Object(w.a)(R.country)?null:{label:R.countryName,value:R.country},onChange:function(e){return t=e,console.log("here is the country",t),F(Object(a.a)(Object(a.a)({},W),{},{country:""})),void G(Object(a.a)(Object(a.a)({},R),{},{country:t.value,countryName:t.label}));var t},options:_,placeholder:"Select Country"}),s.a.createElement(v.a,null,W.country)))),s.a.createElement("div",{className:"d-flex justify-content-end"},s.a.createElement(h.a,{variant:"warning",onClick:function(){try{e.history.push("/vendors")}catch(t){e.onHide()}}},"Cancel"),s.a.createElement(h.a,{disabled:N,variant:"primary",onClick:function(){var t=Object(m.a)(R),n=t.isValid,r=t.errors;if(!n)return console.log(r),void F(Object(a.a)({},r));console.log("no errros"),M(!0);var c={action:"add",first_name:R.fname,last_name:R.lname,middle_name:R.mname,category:parseInt(R.category)||null,email:R.email,website:R.website,tax_number:parseFloat(R.tax),phone1:R.phone1,phone2:R.phone2,address:R.address,country:R.country};console.log(c),Object(j.a)(c).then((function(t){if(console.log(t),t.json.status){M(!1),b.a.fire({icon:"success",title:"Customer created successfully!",background:"#dffff0"});try{e.history.push("/customers")}catch(a){console.log(t.json.customers[0]);var n=t.json.customers[0];e.setCreatedToSelected({value:n.id,label:n.name}),e.onHide()}}else M(!1),b.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"})})).catch((function(e){M(!1),console.log(e)}))}},N?s.a.createElement(s.a.Fragment,null,s.a.createElement("i",{className:"fa fa-spinner text-c-white f-15 fa-pulse m-l-1"}),"Submitting"):"Submit")))))))}},262:function(e,t,n){"use strict";var a=n(0),r=n.n(a),c=n(306),o=n(36);t.a=function(e){return Object(o.a)(e.children)?r.a.createElement("span",null):r.a.createElement(r.a.Fragment,null,r.a.createElement(c.a.Text,{style:{color:"red"}},e.children))}},263:function(e,t,n){"use strict";var a=n(0),r=n.n(a);t.a=function(){return r.a.createElement("div",{className:"loader-bg"},r.a.createElement("div",{className:"loader-track"},r.a.createElement("div",{className:"loader-fill"})))}},264:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),u=n.n(s),i=n(19),l=["xl","lg","md","sm","xs"],p=u.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.as,p=void 0===s?"div":s,h=Object(r.a)(e,["bsPrefix","className","as"]),f=Object(i.b)(n,"col"),d=[],m=[];return l.forEach((function(e){var t,n,a,r=h[e];if(delete h[e],null!=r&&"object"===typeof r){var c=r.span;t=void 0===c||c,n=r.offset,a=r.order}else t=r;var o="xs"!==e?"-"+e:"";null!=t&&d.push(!0===t?""+f+o:""+f+o+"-"+t),null!=a&&m.push("order"+o+"-"+a),null!=n&&m.push("offset"+o+"-"+n)})),d.length||d.push(f),u.a.createElement(p,Object(a.a)({},h,{ref:t,className:o.a.apply(void 0,[c].concat(d,m))}))}));p.displayName="Col",t.a=p},266:function(e,t,n){"use strict";var a=n(6),r=n(0),c=n.n(r),o=n(11),s=n.n(o);t.a=function(e){return c.a.forwardRef((function(t,n){return c.a.createElement("div",Object(a.a)({},t,{ref:n,className:s()(t.className,e)}))}))}},271:function(e,t,n){"use strict";n.d(t,"j",(function(){return y})),n.d(t,"b",(function(){return O})),n.d(t,"o",(function(){return x})),n.d(t,"e",(function(){return j})),n.d(t,"k",(function(){return b})),n.d(t,"i",(function(){return s})),n.d(t,"a",(function(){return i})),n.d(t,"d",(function(){return u})),n.d(t,"n",(function(){return p})),n.d(t,"h",(function(){return l})),n.d(t,"m",(function(){return h})),n.d(t,"c",(function(){return d})),n.d(t,"f",(function(){return f})),n.d(t,"p",(function(){return v})),n.d(t,"l",(function(){return m})),n.d(t,"g",(function(){return w}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discounts/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discounts/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),h=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/taxes/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),f=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/taxes/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),d=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),m=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),v=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),b=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/purchaseorders/status","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),y=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),O=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),j=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),x=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),w=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/user/countries/get ","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},276:function(e,t,n){"use strict";n(308),n(299),n(327),n(309);var a=n(300),r=n(301),c=n(302),o=n(304),s=n(307),u=n(293),i=n(292),l=n(0),p=n.n(l),h=n(317),f=n(312),d=(n(40),n(7),n(303),n(268)),m=(n(289),n(315),n(316),n(331)),v=n(446),b=(l.Component,Object(m.a)(d.a));t.a=b},283:function(e,t,n){"use strict";n.d(t,"d",(function(){return s})),n.d(t,"a",(function(){return u})),n.d(t,"b",(function(){return i})),n.d(t,"e",(function(){return l})),n.d(t,"c",(function(){return p}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/vendors/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/vendor/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/vendors/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/vendor/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/vendor/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},286:function(e,t,n){e.exports=n(288)},288:function(e,t,n){Object.defineProperty(t,"__esModule",{value:!0});var a=n(0);function r(){return(r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e}).apply(this,arguments)}var c=a.createElement("svg",{viewBox:"-2 -5 14 20",height:"100%",width:"100%",style:{position:"absolute",top:0}},a.createElement("path",{d:"M9.9 2.12L7.78 0 4.95 2.828 2.12 0 0 2.12l2.83 2.83L0 7.776 2.123 9.9 4.95 7.07 7.78 9.9 9.9 7.776 7.072 4.95 9.9 2.12",fill:"#fff",fillRule:"evenodd"})),o=a.createElement("svg",{height:"100%",width:"100%",viewBox:"-2 -5 17 21",style:{position:"absolute",top:0}},a.createElement("path",{d:"M11.264 0L5.26 6.004 2.103 2.847 0 4.95l5.26 5.26 8.108-8.107L11.264 0",fill:"#fff",fillRule:"evenodd"}));function s(e){if(7===e.length)return e;for(var t="#",n=1;n<4;n+=1)t+=e[n]+e[n];return t}function u(e,t,n,a,r){return function(e,t,n,a,r){var c=(e-n)/(t-n);if(0===c)return a;if(1===c)return r;for(var o="#",s=1;s<6;s+=2){var u=parseInt(a.substr(s,2),16),i=parseInt(r.substr(s,2),16),l=Math.round((1-c)*u+c*i).toString(16);1===l.length&&(l="0"+l),o+=l}return o}(e,t,n,s(a),s(r))}var i=function(e){function t(t){e.call(this,t);var n=t.height,a=t.width,r=t.checked;this.t=t.handleDiameter||n-2,this.i=Math.max(a-n,a-(n+this.t)/2),this.o=Math.max(0,(n-this.t)/2),this.state={s:r?this.i:this.o},this.n=0,this.e=0,this.h=this.h.bind(this),this.r=this.r.bind(this),this.a=this.a.bind(this),this.c=this.c.bind(this),this.l=this.l.bind(this),this.u=this.u.bind(this),this.f=this.f.bind(this),this.p=this.p.bind(this),this.b=this.b.bind(this),this.g=this.g.bind(this),this.v=this.v.bind(this),this.w=this.w.bind(this)}return e&&(t.__proto__=e),((t.prototype=Object.create(e&&e.prototype)).constructor=t).prototype.componentDidUpdate=function(e){e.checked!==this.props.checked&&this.setState({s:this.props.checked?this.i:this.o})},t.prototype.k=function(e){this.y.focus(),this.setState({C:e,M:!0,m:Date.now()})},t.prototype.x=function(e){var t=this.state,n=t.C,a=t.s,r=(this.props.checked?this.i:this.o)+e-n;t.R||e===n||this.setState({R:!0});var c=Math.min(this.i,Math.max(this.o,r));c!==a&&this.setState({s:c})},t.prototype.S=function(e){var t=this.state,n=t.s,a=t.R,r=t.m,c=this.props.checked,o=(this.i+this.o)/2,s=Date.now()-r;!a||s<250?this.T(e):c?o<n?this.setState({s:this.i}):this.T(e):n<o?this.setState({s:this.o}):this.T(e),this.setState({R:!1,M:!1}),this.n=Date.now()},t.prototype.h=function(e){e.preventDefault(),"number"==typeof e.button&&0!==e.button||(this.k(e.clientX),window.addEventListener("mousemove",this.r),window.addEventListener("mouseup",this.a))},t.prototype.r=function(e){e.preventDefault(),this.x(e.clientX)},t.prototype.a=function(e){this.S(e),window.removeEventListener("mousemove",this.r),window.removeEventListener("mouseup",this.a)},t.prototype.c=function(e){this.$=null,this.k(e.touches[0].clientX)},t.prototype.l=function(e){this.x(e.touches[0].clientX)},t.prototype.u=function(e){e.preventDefault(),this.S(e)},t.prototype.p=function(e){50<Date.now()-this.n&&(this.T(e),50<Date.now()-this.e&&this.setState({M:!1}))},t.prototype.b=function(){this.e=Date.now()},t.prototype.g=function(){this.setState({M:!0})},t.prototype.v=function(){this.setState({M:!1})},t.prototype.w=function(e){this.y=e},t.prototype.f=function(e){e.preventDefault(),this.y.focus(),this.T(e),this.setState({M:!1})},t.prototype.T=function(e){var t=this.props;(0,t.onChange)(!t.checked,e,t.id)},t.prototype.render=function(){var e=this.props,t=e.disabled,n=e.className,c=e.offColor,o=e.onColor,s=e.offHandleColor,i=e.onHandleColor,l=e.checkedIcon,p=e.uncheckedIcon,h=e.boxShadow,f=e.activeBoxShadow,d=e.height,m=e.width,v=function(e,t){var n={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&-1===t.indexOf(a)&&(n[a]=e[a]);return n}(e,["disabled","className","offColor","onColor","offHandleColor","onHandleColor","checkedIcon","uncheckedIcon","boxShadow","activeBoxShadow","height","width","handleDiameter"]),b=this.state,y=b.s,O=b.R,j=b.M,x={position:"relative",display:"inline-block",textAlign:"left",opacity:t?.5:1,direction:"ltr",borderRadius:d/2,WebkitTransition:"opacity 0.25s",MozTransition:"opacity 0.25s",transition:"opacity 0.25s",touchAction:"none",WebkitTapHighlightColor:"rgba(0, 0, 0, 0)",WebkitUserSelect:"none",MozUserSelect:"none",msUserSelect:"none",userSelect:"none"},w={height:d,width:m,margin:Math.max(0,(this.t-d)/2),position:"relative",background:u(y,this.i,this.o,c,o),borderRadius:d/2,cursor:t?"default":"pointer",WebkitTransition:O?null:"background 0.25s",MozTransition:O?null:"background 0.25s",transition:O?null:"background 0.25s"},g={height:d,width:Math.min(1.5*d,m-(this.t+d)/2+1),position:"relative",opacity:(y-this.o)/(this.i-this.o),pointerEvents:"none",WebkitTransition:O?null:"opacity 0.25s",MozTransition:O?null:"opacity 0.25s",transition:O?null:"opacity 0.25s"},E={height:d,width:Math.min(1.5*d,m-(this.t+d)/2+1),position:"absolute",opacity:1-(y-this.o)/(this.i-this.o),right:0,top:0,pointerEvents:"none",WebkitTransition:O?null:"opacity 0.25s",MozTransition:O?null:"opacity 0.25s",transition:O?null:"opacity 0.25s"},k={height:this.t,width:this.t,background:u(y,this.i,this.o,s,i),display:"inline-block",cursor:t?"default":"pointer",borderRadius:"50%",position:"absolute",transform:"translateX("+y+"px)",top:Math.max(0,(d-this.t)/2),outline:0,boxShadow:j?f:h,border:0,WebkitTransition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s",MozTransition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s",transition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s"};return a.createElement("div",{className:n,style:x},a.createElement("div",{className:"react-switch-bg",style:w,onClick:t?null:this.f,onMouseDown:function(e){return e.preventDefault()}},l&&a.createElement("div",{style:g},l),p&&a.createElement("div",{style:E},p)),a.createElement("div",{className:"react-switch-handle",style:k,onClick:function(e){return e.preventDefault()},onMouseDown:t?null:this.h,onTouchStart:t?null:this.c,onTouchMove:t?null:this.l,onTouchEnd:t?null:this.u,onTouchCancel:t?null:this.v}),a.createElement("input",r({},{type:"checkbox",role:"switch",disabled:t,style:{border:0,clip:"rect(0 0 0 0)",height:1,margin:-1,overflow:"hidden",padding:0,position:"absolute",width:1}},v,{ref:this.w,onFocus:this.g,onBlur:this.v,onKeyUp:this.b,onChange:this.p})))},t}(a.Component);i.defaultProps={disabled:!1,offColor:"#888",onColor:"#080",offHandleColor:"#fff",onHandleColor:"#fff",uncheckedIcon:c,checkedIcon:o,boxShadow:null,activeBoxShadow:"0 0 2px 3px #3bf",height:28,width:56},t.default=i},296:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),u=n.n(s),i=n(19),l=["xl","lg","md","sm","xs"],p=u.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.noGutters,p=e.as,h=void 0===p?"div":p,f=Object(r.a)(e,["bsPrefix","className","noGutters","as"]),d=Object(i.b)(n,"row"),m=d+"-cols",v=[];return l.forEach((function(e){var t,n=f[e];delete f[e];var a="xs"!==e?"-"+e:"";null!=(t=null!=n&&"object"===typeof n?n.cols:n)&&v.push(""+m+a+"-"+t)})),u.a.createElement(h,Object(a.a)({ref:t},f,{className:o.a.apply(void 0,[c,d,s&&"no-gutters"].concat(v))}))}));p.displayName="Row",p.defaultProps={noGutters:!1},t.a=p},311:function(e,t,n){"use strict";n.d(t,"d",(function(){return s})),n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return u})),n.d(t,"e",(function(){return p})),n.d(t,"c",(function(){return l}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},313:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),u=n.n(s),i=n(19),l=n(66),p=n(266),h=n(84),f=u.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.variant,l=e.as,p=void 0===l?"img":l,h=Object(r.a)(e,["bsPrefix","className","variant","as"]),f=Object(i.b)(n,"card-img");return u.a.createElement(p,Object(a.a)({ref:t,className:o()(s?f+"-"+s:f,c)},h))}));f.displayName="CardImg",f.defaultProps={variant:null};var d=f,m=Object(p.a)("h5"),v=Object(p.a)("h6"),b=Object(l.a)("card-body"),y=u.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,l=e.bg,p=e.text,f=e.border,d=e.body,m=e.children,v=e.as,y=void 0===v?"div":v,O=Object(r.a)(e,["bsPrefix","className","bg","text","border","body","children","as"]),j=Object(i.b)(n,"card"),x=Object(s.useMemo)((function(){return{cardHeaderBsPrefix:j+"-header"}}),[j]);return u.a.createElement(h.a.Provider,{value:x},u.a.createElement(y,Object(a.a)({ref:t},O,{className:o()(c,j,l&&"bg-"+l,p&&"text-"+p,f&&"border-"+f)}),d?u.a.createElement(b,null,m):m))}));y.displayName="Card",y.defaultProps={body:!1},y.Img=d,y.Title=Object(l.a)("card-title",{Component:m}),y.Subtitle=Object(l.a)("card-subtitle",{Component:v}),y.Body=b,y.Link=Object(l.a)("card-link",{Component:"a"}),y.Text=Object(l.a)("card-text",{Component:"p"}),y.Header=Object(l.a)("card-header"),y.Footer=Object(l.a)("card-footer"),y.ImgOverlay=Object(l.a)("card-img-overlay");t.a=y},431:function(e,t,n){"use strict";n.d(t,"d",(function(){return p})),n.d(t,"c",(function(){return s})),n.d(t,"a",(function(){return l})),n.d(t,"b",(function(){return u})),n.d(t,"e",(function(){return i}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},451:function(e,t,n){"use strict";n.d(t,"a",(function(){return r}));var a=n(36),r=function(e){var t={};return Object(a.a)(e.fname)&&(t.fname="First Name cannot be empty."),Object(a.a)(e.lname)&&(t.lname="Last Name cannot be empty."),Object(a.a)(e.email)&&(t.email="Email cannot be empty."),e.email&&!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(e.email)&&(t.email="Email not valid."),Object(a.a)(e.phone1)&&(t.phone1="Atleast, a phone number should be provided."),{isValid:Object(a.a)(t),errors:t}}}}]);
//# sourceMappingURL=44.96064c54.chunk.js.map