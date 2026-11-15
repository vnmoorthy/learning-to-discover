import{r as ke,s as Ud,g as Bx,j as Ti,_ as Nd}from"./vendor-P-kBGxpi.js";/**
 * @license
 * Copyright 2010-2024 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const Ja="170",gs={LEFT:0,MIDDLE:1,RIGHT:2,ROTATE:0,DOLLY:1,PAN:2},vs={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},Rv=0,Od=1,Pv=2,zx=3,Iv=0,Ku=1,Ea=2,wi=3,vr=0,Vn=1,Gi=2,mr=0,Ts=1,Fd=2,Bd=3,zd=4,Lv=5,zr=100,Dv=101,Uv=102,Nv=103,Ov=104,Fv=200,Bv=201,zv=202,kv=203,cu=204,uu=205,Hv=206,Vv=207,Gv=208,Wv=209,Xv=210,Yv=211,qv=212,Zv=213,jv=214,hu=0,fu=1,du=2,Is=3,pu=4,mu=5,gu=6,vu=7,Ka=0,Jv=1,Kv=2,qi=0,Qv=1,$v=2,e_=3,tp=4,t_=5,n_=6,i_=7,kd="attached",r_="detached",Qu=300,_r=301,Hr=302,Da=303,Ua=304,Oo=306,Na=1e3,vi=1001,Oa=1002,wn=1003,np=1004,kx=1004,wo=1005,Hx=1005,cn=1006,wa=1007,Vx=1007,Xi=1008,Gx=1008,bi=1009,ip=1010,rp=1011,Io=1012,$u=1013,yr=1014,Kn=1015,Fo=1016,eh=1017,th=1018,Ls=1020,sp=35902,op=1021,ap=1022,Dn=1023,lp=1024,cp=1025,As=1026,Ds=1027,nh=1028,Qa=1029,up=1030,ih=1031,Wx=1032,rh=1033,Ta=33776,Aa=33777,ba=33778,Ca=33779,_u=35840,yu=35841,xu=35842,Su=35843,Mu=36196,Eu=37492,wu=37496,Tu=37808,Au=37809,bu=37810,Cu=37811,Ru=37812,Pu=37813,Iu=37814,Lu=37815,Du=37816,Uu=37817,Nu=37818,Ou=37819,Fu=37820,Bu=37821,Ra=36492,zu=36494,ku=36495,hp=36283,Hu=36284,Vu=36285,Gu=36286,s_=2200,o_=2201,a_=2202,Fa=2300,Wu=2301,ou=2302,Ss=2400,Ms=2401,Ba=2402,sh=2500,fp=2501,Xx=0,Yx=1,qx=2,l_=3200,c_=3201,Zx=3202,jx=3203,Gr=0,u_=1,fr="",jn="srgb",Ns="srgb-linear",$a="linear",Ft="srgb",Jx=0,_s=7680,Kx=7681,Qx=7682,$x=7683,eS=34055,tS=34056,nS=5386,iS=512,rS=513,sS=514,oS=515,aS=516,lS=517,cS=518,Hd=519,h_=512,f_=513,d_=514,dp=515,p_=516,m_=517,g_=518,v_=519,za=35044,uS=35048,hS=35040,fS=35045,dS=35049,pS=35041,mS=35046,gS=35050,vS=35042,_S="100",Vd="300 es",Yi=2e3,ka=2001;let Ji=class{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const n=this._listeners;n[e]===void 0&&(n[e]=[]),n[e].indexOf(t)===-1&&n[e].push(t)}hasEventListener(e,t){if(this._listeners===void 0)return!1;const n=this._listeners;return n[e]!==void 0&&n[e].indexOf(t)!==-1}removeEventListener(e,t){if(this._listeners===void 0)return;const i=this._listeners[e];if(i!==void 0){const s=i.indexOf(t);s!==-1&&i.splice(s,1)}}dispatchEvent(e){if(this._listeners===void 0)return;const n=this._listeners[e.type];if(n!==void 0){e.target=this;const i=n.slice(0);for(let s=0,l=i.length;s<l;s++)i[s].call(this,e);e.target=null}}};const Pn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"];let bg=1234567;const bs=Math.PI/180,Lo=180/Math.PI;function oi(){const r=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,n=Math.random()*4294967295|0;return(Pn[r&255]+Pn[r>>8&255]+Pn[r>>16&255]+Pn[r>>24&255]+"-"+Pn[e&255]+Pn[e>>8&255]+"-"+Pn[e>>16&15|64]+Pn[e>>24&255]+"-"+Pn[t&63|128]+Pn[t>>8&255]+"-"+Pn[t>>16&255]+Pn[t>>24&255]+Pn[n&255]+Pn[n>>8&255]+Pn[n>>16&255]+Pn[n>>24&255]).toLowerCase()}function Jt(r,e,t){return Math.max(e,Math.min(t,r))}function pp(r,e){return(r%e+e)%e}function yS(r,e,t,n,i){return n+(r-e)*(i-n)/(t-e)}function xS(r,e,t){return r!==e?(t-r)/(e-r):0}function Pa(r,e,t){return(1-t)*r+t*e}function SS(r,e,t,n){return Pa(r,e,1-Math.exp(-t*n))}function MS(r,e=1){return e-Math.abs(pp(r,e*2)-e)}function ES(r,e,t){return r<=e?0:r>=t?1:(r=(r-e)/(t-e),r*r*(3-2*r))}function wS(r,e,t){return r<=e?0:r>=t?1:(r=(r-e)/(t-e),r*r*r*(r*(r*6-15)+10))}function TS(r,e){return r+Math.floor(Math.random()*(e-r+1))}function AS(r,e){return r+Math.random()*(e-r)}function bS(r){return r*(.5-Math.random())}function CS(r){r!==void 0&&(bg=r);let e=bg+=1831565813;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}function RS(r){return r*bs}function PS(r){return r*Lo}function IS(r){return(r&r-1)===0&&r!==0}function LS(r){return Math.pow(2,Math.ceil(Math.log(r)/Math.LN2))}function DS(r){return Math.pow(2,Math.floor(Math.log(r)/Math.LN2))}function US(r,e,t,n,i){const s=Math.cos,l=Math.sin,c=s(t/2),u=l(t/2),h=s((e+n)/2),f=l((e+n)/2),p=s((e-n)/2),m=l((e-n)/2),g=s((n-e)/2),y=l((n-e)/2);switch(i){case"XYX":r.set(c*f,u*p,u*m,c*h);break;case"YZY":r.set(u*m,c*f,u*p,c*h);break;case"ZXZ":r.set(u*p,u*m,c*f,c*h);break;case"XZX":r.set(c*f,u*y,u*g,c*h);break;case"YXY":r.set(u*g,c*f,u*y,c*h);break;case"ZYZ":r.set(u*y,u*g,c*f,c*h);break;default:console.warn("THREE.MathUtils: .setQuaternionFromProperEuler() encountered an unknown order: "+i)}}function Hn(r,e){switch(e.constructor){case Float32Array:return r;case Uint32Array:return r/4294967295;case Uint16Array:return r/65535;case Uint8Array:return r/255;case Int32Array:return Math.max(r/2147483647,-1);case Int16Array:return Math.max(r/32767,-1);case Int8Array:return Math.max(r/127,-1);default:throw new Error("Invalid component type.")}}function vt(r,e){switch(e.constructor){case Float32Array:return r;case Uint32Array:return Math.round(r*4294967295);case Uint16Array:return Math.round(r*65535);case Uint8Array:return Math.round(r*255);case Int32Array:return Math.round(r*2147483647);case Int16Array:return Math.round(r*32767);case Int8Array:return Math.round(r*127);default:throw new Error("Invalid component type.")}}const __={DEG2RAD:bs,RAD2DEG:Lo,generateUUID:oi,clamp:Jt,euclideanModulo:pp,mapLinear:yS,inverseLerp:xS,lerp:Pa,damp:SS,pingpong:MS,smoothstep:ES,smootherstep:wS,randInt:TS,randFloat:AS,randFloatSpread:bS,seededRandom:CS,degToRad:RS,radToDeg:PS,isPowerOfTwo:IS,ceilPowerOfTwo:LS,floorPowerOfTwo:DS,setQuaternionFromProperEuler:US,normalize:vt,denormalize:Hn};class ae{constructor(e=0,t=0){ae.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,n=this.y,i=e.elements;return this.x=i[0]*t+i[3]*n+i[6],this.y=i[1]*t+i[4]*n+i[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=Math.max(e.x,Math.min(t.x,this.x)),this.y=Math.max(e.y,Math.min(t.y,this.y)),this}clampScalar(e,t){return this.x=Math.max(e,Math.min(t,this.x)),this.y=Math.max(e,Math.min(t,this.y)),this}clampLength(e,t){const n=this.length();return this.divideScalar(n||1).multiplyScalar(Math.max(e,Math.min(t,n)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const n=this.dot(e)/t;return Math.acos(Jt(n,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,n=this.y-e.y;return t*t+n*n}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const n=Math.cos(t),i=Math.sin(t),s=this.x-e.x,l=this.y-e.y;return this.x=s*n-l*i+e.x,this.y=s*i+l*n+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class gt{constructor(e,t,n,i,s,l,c,u,h){gt.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,n,i,s,l,c,u,h)}set(e,t,n,i,s,l,c,u,h){const f=this.elements;return f[0]=e,f[1]=i,f[2]=c,f[3]=t,f[4]=s,f[5]=u,f[6]=n,f[7]=l,f[8]=h,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,n=e.elements;return t[0]=n[0],t[1]=n[1],t[2]=n[2],t[3]=n[3],t[4]=n[4],t[5]=n[5],t[6]=n[6],t[7]=n[7],t[8]=n[8],this}extractBasis(e,t,n){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),n.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const n=e.elements,i=t.elements,s=this.elements,l=n[0],c=n[3],u=n[6],h=n[1],f=n[4],p=n[7],m=n[2],g=n[5],y=n[8],M=i[0],x=i[3],_=i[6],w=i[1],E=i[4],T=i[7],U=i[2],P=i[5],D=i[8];return s[0]=l*M+c*w+u*U,s[3]=l*x+c*E+u*P,s[6]=l*_+c*T+u*D,s[1]=h*M+f*w+p*U,s[4]=h*x+f*E+p*P,s[7]=h*_+f*T+p*D,s[2]=m*M+g*w+y*U,s[5]=m*x+g*E+y*P,s[8]=m*_+g*T+y*D,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],n=e[1],i=e[2],s=e[3],l=e[4],c=e[5],u=e[6],h=e[7],f=e[8];return t*l*f-t*c*h-n*s*f+n*c*u+i*s*h-i*l*u}invert(){const e=this.elements,t=e[0],n=e[1],i=e[2],s=e[3],l=e[4],c=e[5],u=e[6],h=e[7],f=e[8],p=f*l-c*h,m=c*u-f*s,g=h*s-l*u,y=t*p+n*m+i*g;if(y===0)return this.set(0,0,0,0,0,0,0,0,0);const M=1/y;return e[0]=p*M,e[1]=(i*h-f*n)*M,e[2]=(c*n-i*l)*M,e[3]=m*M,e[4]=(f*t-i*u)*M,e[5]=(i*s-c*t)*M,e[6]=g*M,e[7]=(n*u-h*t)*M,e[8]=(l*t-n*s)*M,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,n,i,s,l,c){const u=Math.cos(s),h=Math.sin(s);return this.set(n*u,n*h,-n*(u*l+h*c)+l+e,-i*h,i*u,-i*(-h*l+u*c)+c+t,0,0,1),this}scale(e,t){return this.premultiply(Nf.makeScale(e,t)),this}rotate(e){return this.premultiply(Nf.makeRotation(-e)),this}translate(e,t){return this.premultiply(Nf.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),n=Math.sin(e);return this.set(t,-n,0,n,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,n=e.elements;for(let i=0;i<9;i++)if(t[i]!==n[i])return!1;return!0}fromArray(e,t=0){for(let n=0;n<9;n++)this.elements[n]=e[n+t];return this}toArray(e=[],t=0){const n=this.elements;return e[t]=n[0],e[t+1]=n[1],e[t+2]=n[2],e[t+3]=n[3],e[t+4]=n[4],e[t+5]=n[5],e[t+6]=n[6],e[t+7]=n[7],e[t+8]=n[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Nf=new gt;function y_(r){for(let e=r.length-1;e>=0;--e)if(r[e]>=65535)return!0;return!1}const NS={Int8Array,Uint8Array,Uint8ClampedArray,Int16Array,Uint16Array,Int32Array,Uint32Array,Float32Array,Float64Array};function To(r,e){return new NS[r](e)}function Ha(r){return document.createElementNS("http://www.w3.org/1999/xhtml",r)}function x_(){const r=Ha("canvas");return r.style.display="block",r}const Cg={};function xa(r){r in Cg||(Cg[r]=!0,console.warn(r))}function OS(r,e,t){return new Promise(function(n,i){function s(){switch(r.clientWaitSync(e,r.SYNC_FLUSH_COMMANDS_BIT,0)){case r.WAIT_FAILED:i();break;case r.TIMEOUT_EXPIRED:setTimeout(s,t);break;default:n()}}setTimeout(s,t)})}function FS(r){const e=r.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function BS(r){const e=r.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const Pt={enabled:!0,workingColorSpace:Ns,spaces:{},convert:function(r,e,t){return this.enabled===!1||e===t||!e||!t||(this.spaces[e].transfer===Ft&&(r.r=gr(r.r),r.g=gr(r.g),r.b=gr(r.b)),this.spaces[e].primaries!==this.spaces[t].primaries&&(r.applyMatrix3(this.spaces[e].toXYZ),r.applyMatrix3(this.spaces[t].fromXYZ)),this.spaces[t].transfer===Ft&&(r.r=Po(r.r),r.g=Po(r.g),r.b=Po(r.b))),r},fromWorkingColorSpace:function(r,e){return this.convert(r,this.workingColorSpace,e)},toWorkingColorSpace:function(r,e){return this.convert(r,e,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===fr?$a:this.spaces[r].transfer},getLuminanceCoefficients:function(r,e=this.workingColorSpace){return r.fromArray(this.spaces[e].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,e,t){return r.copy(this.spaces[e].toXYZ).multiply(this.spaces[t].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}};function gr(r){return r<.04045?r*.0773993808:Math.pow(r*.9478672986+.0521327014,2.4)}function Po(r){return r<.0031308?r*12.92:1.055*Math.pow(r,.41666)-.055}const Rg=[.64,.33,.3,.6,.15,.06],Pg=[.2126,.7152,.0722],Ig=[.3127,.329],Lg=new gt().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),Dg=new gt().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);Pt.define({[Ns]:{primaries:Rg,whitePoint:Ig,transfer:$a,toXYZ:Lg,fromXYZ:Dg,luminanceCoefficients:Pg,workingColorSpaceConfig:{unpackColorSpace:jn},outputColorSpaceConfig:{drawingBufferColorSpace:jn}},[jn]:{primaries:Rg,whitePoint:Ig,transfer:Ft,toXYZ:Lg,fromXYZ:Dg,luminanceCoefficients:Pg,outputColorSpaceConfig:{drawingBufferColorSpace:jn}}});let to;class S_{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{to===void 0&&(to=Ha("canvas")),to.width=e.width,to.height=e.height;const n=to.getContext("2d");e instanceof ImageData?n.putImageData(e,0,0):n.drawImage(e,0,0,e.width,e.height),t=to}return t.width>2048||t.height>2048?(console.warn("THREE.ImageUtils.getDataURL: Image converted to jpg for performance reasons",e),t.toDataURL("image/jpeg",.6)):t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Ha("canvas");t.width=e.width,t.height=e.height;const n=t.getContext("2d");n.drawImage(e,0,0,e.width,e.height);const i=n.getImageData(0,0,e.width,e.height),s=i.data;for(let l=0;l<s.length;l++)s[l]=gr(s[l]/255)*255;return n.putImageData(i,0,0),t}else if(e.data){const t=e.data.slice(0);for(let n=0;n<t.length;n++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[n]=Math.floor(gr(t[n]/255)*255):t[n]=gr(t[n]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let zS=0;class Es{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:zS++}),this.uuid=oi(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const n={uuid:this.uuid,url:""},i=this.data;if(i!==null){let s;if(Array.isArray(i)){s=[];for(let l=0,c=i.length;l<c;l++)i[l].isDataTexture?s.push(Of(i[l].image)):s.push(Of(i[l]))}else s=Of(i);n.url=s}return t||(e.images[this.uuid]=n),n}}function Of(r){return typeof HTMLImageElement<"u"&&r instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&r instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&r instanceof ImageBitmap?S_.getDataURL(r):r.data?{data:Array.from(r.data),width:r.width,height:r.height,type:r.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let kS=0;class Kt extends Ji{constructor(e=Kt.DEFAULT_IMAGE,t=Kt.DEFAULT_MAPPING,n=vi,i=vi,s=cn,l=Xi,c=Dn,u=bi,h=Kt.DEFAULT_ANISOTROPY,f=fr){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:kS++}),this.uuid=oi(),this.name="",this.source=new Es(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=n,this.wrapT=i,this.magFilter=s,this.minFilter=l,this.anisotropy=h,this.format=c,this.internalFormat=null,this.type=u,this.offset=new ae(0,0),this.repeat=new ae(1,1),this.center=new ae(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new gt,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=f,this.userData={},this.version=0,this.onUpdate=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const n={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(n.userData=this.userData),t||(e.textures[this.uuid]=n),n}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Qu)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Na:e.x=e.x-Math.floor(e.x);break;case vi:e.x=e.x<0?0:1;break;case Oa:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Na:e.y=e.y-Math.floor(e.y);break;case vi:e.y=e.y<0?0:1;break;case Oa:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}Kt.DEFAULT_IMAGE=null;Kt.DEFAULT_MAPPING=Qu;Kt.DEFAULT_ANISOTROPY=1;class At{constructor(e=0,t=0,n=0,i=1){At.prototype.isVector4=!0,this.x=e,this.y=t,this.z=n,this.w=i}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,n,i){return this.x=e,this.y=t,this.z=n,this.w=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,n=this.y,i=this.z,s=this.w,l=e.elements;return this.x=l[0]*t+l[4]*n+l[8]*i+l[12]*s,this.y=l[1]*t+l[5]*n+l[9]*i+l[13]*s,this.z=l[2]*t+l[6]*n+l[10]*i+l[14]*s,this.w=l[3]*t+l[7]*n+l[11]*i+l[15]*s,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,n,i,s;const u=e.elements,h=u[0],f=u[4],p=u[8],m=u[1],g=u[5],y=u[9],M=u[2],x=u[6],_=u[10];if(Math.abs(f-m)<.01&&Math.abs(p-M)<.01&&Math.abs(y-x)<.01){if(Math.abs(f+m)<.1&&Math.abs(p+M)<.1&&Math.abs(y+x)<.1&&Math.abs(h+g+_-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const E=(h+1)/2,T=(g+1)/2,U=(_+1)/2,P=(f+m)/4,D=(p+M)/4,F=(y+x)/4;return E>T&&E>U?E<.01?(n=0,i=.707106781,s=.707106781):(n=Math.sqrt(E),i=P/n,s=D/n):T>U?T<.01?(n=.707106781,i=0,s=.707106781):(i=Math.sqrt(T),n=P/i,s=F/i):U<.01?(n=.707106781,i=.707106781,s=0):(s=Math.sqrt(U),n=D/s,i=F/s),this.set(n,i,s,t),this}let w=Math.sqrt((x-y)*(x-y)+(p-M)*(p-M)+(m-f)*(m-f));return Math.abs(w)<.001&&(w=1),this.x=(x-y)/w,this.y=(p-M)/w,this.z=(m-f)/w,this.w=Math.acos((h+g+_-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=Math.max(e.x,Math.min(t.x,this.x)),this.y=Math.max(e.y,Math.min(t.y,this.y)),this.z=Math.max(e.z,Math.min(t.z,this.z)),this.w=Math.max(e.w,Math.min(t.w,this.w)),this}clampScalar(e,t){return this.x=Math.max(e,Math.min(t,this.x)),this.y=Math.max(e,Math.min(t,this.y)),this.z=Math.max(e,Math.min(t,this.z)),this.w=Math.max(e,Math.min(t,this.w)),this}clampLength(e,t){const n=this.length();return this.divideScalar(n||1).multiplyScalar(Math.max(e,Math.min(t,n)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this.z=e.z+(t.z-e.z)*n,this.w=e.w+(t.w-e.w)*n,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class M_ extends Ji{constructor(e=1,t=1,n={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new At(0,0,e,t),this.scissorTest=!1,this.viewport=new At(0,0,e,t);const i={width:e,height:t,depth:1};n=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:cn,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},n);const s=new Kt(i,n.mapping,n.wrapS,n.wrapT,n.magFilter,n.minFilter,n.format,n.type,n.anisotropy,n.colorSpace);s.flipY=!1,s.generateMipmaps=n.generateMipmaps,s.internalFormat=n.internalFormat,this.textures=[];const l=n.count;for(let c=0;c<l;c++)this.textures[c]=s.clone(),this.textures[c].isRenderTargetTexture=!0;this.depthBuffer=n.depthBuffer,this.stencilBuffer=n.stencilBuffer,this.resolveDepthBuffer=n.resolveDepthBuffer,this.resolveStencilBuffer=n.resolveStencilBuffer,this.depthTexture=n.depthTexture,this.samples=n.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}setSize(e,t,n=1){if(this.width!==e||this.height!==t||this.depth!==n){this.width=e,this.height=t,this.depth=n;for(let i=0,s=this.textures.length;i<s;i++)this.textures[i].image.width=e,this.textures[i].image.height=t,this.textures[i].image.depth=n;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let n=0,i=e.textures.length;n<i;n++)this.textures[n]=e.textures[n].clone(),this.textures[n].isRenderTargetTexture=!0;const t=Object.assign({},e.texture.image);return this.texture.source=new Es(t),this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class Ci extends M_{constructor(e=1,t=1,n={}){super(e,t,n),this.isWebGLRenderTarget=!0}}class oh extends Kt{constructor(e=null,t=1,n=1,i=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:n,depth:i},this.magFilter=wn,this.minFilter=wn,this.wrapR=vi,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class HS extends Ci{constructor(e=1,t=1,n=1,i={}){super(e,t,i),this.isWebGLArrayRenderTarget=!0,this.depth=n,this.texture=new oh(null,e,t,n),this.texture.isRenderTargetTexture=!0}}class mp extends Kt{constructor(e=null,t=1,n=1,i=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:n,depth:i},this.magFilter=wn,this.minFilter=wn,this.wrapR=vi,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class VS extends Ci{constructor(e=1,t=1,n=1,i={}){super(e,t,i),this.isWebGL3DRenderTarget=!0,this.depth=n,this.texture=new mp(null,e,t,n),this.texture.isRenderTargetTexture=!0}}class Un{constructor(e=0,t=0,n=0,i=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=n,this._w=i}static slerpFlat(e,t,n,i,s,l,c){let u=n[i+0],h=n[i+1],f=n[i+2],p=n[i+3];const m=s[l+0],g=s[l+1],y=s[l+2],M=s[l+3];if(c===0){e[t+0]=u,e[t+1]=h,e[t+2]=f,e[t+3]=p;return}if(c===1){e[t+0]=m,e[t+1]=g,e[t+2]=y,e[t+3]=M;return}if(p!==M||u!==m||h!==g||f!==y){let x=1-c;const _=u*m+h*g+f*y+p*M,w=_>=0?1:-1,E=1-_*_;if(E>Number.EPSILON){const U=Math.sqrt(E),P=Math.atan2(U,_*w);x=Math.sin(x*P)/U,c=Math.sin(c*P)/U}const T=c*w;if(u=u*x+m*T,h=h*x+g*T,f=f*x+y*T,p=p*x+M*T,x===1-c){const U=1/Math.sqrt(u*u+h*h+f*f+p*p);u*=U,h*=U,f*=U,p*=U}}e[t]=u,e[t+1]=h,e[t+2]=f,e[t+3]=p}static multiplyQuaternionsFlat(e,t,n,i,s,l){const c=n[i],u=n[i+1],h=n[i+2],f=n[i+3],p=s[l],m=s[l+1],g=s[l+2],y=s[l+3];return e[t]=c*y+f*p+u*g-h*m,e[t+1]=u*y+f*m+h*p-c*g,e[t+2]=h*y+f*g+c*m-u*p,e[t+3]=f*y-c*p-u*m-h*g,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,n,i){return this._x=e,this._y=t,this._z=n,this._w=i,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const n=e._x,i=e._y,s=e._z,l=e._order,c=Math.cos,u=Math.sin,h=c(n/2),f=c(i/2),p=c(s/2),m=u(n/2),g=u(i/2),y=u(s/2);switch(l){case"XYZ":this._x=m*f*p+h*g*y,this._y=h*g*p-m*f*y,this._z=h*f*y+m*g*p,this._w=h*f*p-m*g*y;break;case"YXZ":this._x=m*f*p+h*g*y,this._y=h*g*p-m*f*y,this._z=h*f*y-m*g*p,this._w=h*f*p+m*g*y;break;case"ZXY":this._x=m*f*p-h*g*y,this._y=h*g*p+m*f*y,this._z=h*f*y+m*g*p,this._w=h*f*p-m*g*y;break;case"ZYX":this._x=m*f*p-h*g*y,this._y=h*g*p+m*f*y,this._z=h*f*y-m*g*p,this._w=h*f*p+m*g*y;break;case"YZX":this._x=m*f*p+h*g*y,this._y=h*g*p+m*f*y,this._z=h*f*y-m*g*p,this._w=h*f*p-m*g*y;break;case"XZY":this._x=m*f*p-h*g*y,this._y=h*g*p-m*f*y,this._z=h*f*y+m*g*p,this._w=h*f*p+m*g*y;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+l)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const n=t/2,i=Math.sin(n);return this._x=e.x*i,this._y=e.y*i,this._z=e.z*i,this._w=Math.cos(n),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,n=t[0],i=t[4],s=t[8],l=t[1],c=t[5],u=t[9],h=t[2],f=t[6],p=t[10],m=n+c+p;if(m>0){const g=.5/Math.sqrt(m+1);this._w=.25/g,this._x=(f-u)*g,this._y=(s-h)*g,this._z=(l-i)*g}else if(n>c&&n>p){const g=2*Math.sqrt(1+n-c-p);this._w=(f-u)/g,this._x=.25*g,this._y=(i+l)/g,this._z=(s+h)/g}else if(c>p){const g=2*Math.sqrt(1+c-n-p);this._w=(s-h)/g,this._x=(i+l)/g,this._y=.25*g,this._z=(u+f)/g}else{const g=2*Math.sqrt(1+p-n-c);this._w=(l-i)/g,this._x=(s+h)/g,this._y=(u+f)/g,this._z=.25*g}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let n=e.dot(t)+1;return n<Number.EPSILON?(n=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=n):(this._x=0,this._y=-e.z,this._z=e.y,this._w=n)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=n),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(Jt(this.dot(e),-1,1)))}rotateTowards(e,t){const n=this.angleTo(e);if(n===0)return this;const i=Math.min(1,t/n);return this.slerp(e,i),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const n=e._x,i=e._y,s=e._z,l=e._w,c=t._x,u=t._y,h=t._z,f=t._w;return this._x=n*f+l*c+i*h-s*u,this._y=i*f+l*u+s*c-n*h,this._z=s*f+l*h+n*u-i*c,this._w=l*f-n*c-i*u-s*h,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const n=this._x,i=this._y,s=this._z,l=this._w;let c=l*e._w+n*e._x+i*e._y+s*e._z;if(c<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,c=-c):this.copy(e),c>=1)return this._w=l,this._x=n,this._y=i,this._z=s,this;const u=1-c*c;if(u<=Number.EPSILON){const g=1-t;return this._w=g*l+t*this._w,this._x=g*n+t*this._x,this._y=g*i+t*this._y,this._z=g*s+t*this._z,this.normalize(),this}const h=Math.sqrt(u),f=Math.atan2(h,c),p=Math.sin((1-t)*f)/h,m=Math.sin(t*f)/h;return this._w=l*p+this._w*m,this._x=n*p+this._x*m,this._y=i*p+this._y*m,this._z=s*p+this._z*m,this._onChangeCallback(),this}slerpQuaternions(e,t,n){return this.copy(e).slerp(t,n)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),n=Math.random(),i=Math.sqrt(1-n),s=Math.sqrt(n);return this.set(i*Math.sin(e),i*Math.cos(e),s*Math.sin(t),s*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class L{constructor(e=0,t=0,n=0){L.prototype.isVector3=!0,this.x=e,this.y=t,this.z=n}set(e,t,n){return n===void 0&&(n=this.z),this.x=e,this.y=t,this.z=n,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(Ug.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(Ug.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,n=this.y,i=this.z,s=e.elements;return this.x=s[0]*t+s[3]*n+s[6]*i,this.y=s[1]*t+s[4]*n+s[7]*i,this.z=s[2]*t+s[5]*n+s[8]*i,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,n=this.y,i=this.z,s=e.elements,l=1/(s[3]*t+s[7]*n+s[11]*i+s[15]);return this.x=(s[0]*t+s[4]*n+s[8]*i+s[12])*l,this.y=(s[1]*t+s[5]*n+s[9]*i+s[13])*l,this.z=(s[2]*t+s[6]*n+s[10]*i+s[14])*l,this}applyQuaternion(e){const t=this.x,n=this.y,i=this.z,s=e.x,l=e.y,c=e.z,u=e.w,h=2*(l*i-c*n),f=2*(c*t-s*i),p=2*(s*n-l*t);return this.x=t+u*h+l*p-c*f,this.y=n+u*f+c*h-s*p,this.z=i+u*p+s*f-l*h,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,n=this.y,i=this.z,s=e.elements;return this.x=s[0]*t+s[4]*n+s[8]*i,this.y=s[1]*t+s[5]*n+s[9]*i,this.z=s[2]*t+s[6]*n+s[10]*i,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=Math.max(e.x,Math.min(t.x,this.x)),this.y=Math.max(e.y,Math.min(t.y,this.y)),this.z=Math.max(e.z,Math.min(t.z,this.z)),this}clampScalar(e,t){return this.x=Math.max(e,Math.min(t,this.x)),this.y=Math.max(e,Math.min(t,this.y)),this.z=Math.max(e,Math.min(t,this.z)),this}clampLength(e,t){const n=this.length();return this.divideScalar(n||1).multiplyScalar(Math.max(e,Math.min(t,n)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this.z=e.z+(t.z-e.z)*n,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const n=e.x,i=e.y,s=e.z,l=t.x,c=t.y,u=t.z;return this.x=i*u-s*c,this.y=s*l-n*u,this.z=n*c-i*l,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const n=e.dot(this)/t;return this.copy(e).multiplyScalar(n)}projectOnPlane(e){return Ff.copy(this).projectOnVector(e),this.sub(Ff)}reflect(e){return this.sub(Ff.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const n=this.dot(e)/t;return Math.acos(Jt(n,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,n=this.y-e.y,i=this.z-e.z;return t*t+n*n+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,n){const i=Math.sin(t)*e;return this.x=i*Math.sin(n),this.y=Math.cos(t)*e,this.z=i*Math.cos(n),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,n){return this.x=e*Math.sin(t),this.y=n,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),n=this.setFromMatrixColumn(e,1).length(),i=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=n,this.z=i,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,n=Math.sqrt(1-t*t);return this.x=n*Math.cos(e),this.y=t,this.z=n*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const Ff=new L,Ug=new Un;class _n{constructor(e=new L(1/0,1/0,1/0),t=new L(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,n=e.length;t<n;t+=3)this.expandByPoint(Si.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,n=e.count;t<n;t++)this.expandByPoint(Si.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,n=e.length;t<n;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const n=Si.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(n),this.max.copy(e).add(n),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const n=e.geometry;if(n!==void 0){const s=n.getAttribute("position");if(t===!0&&s!==void 0&&e.isInstancedMesh!==!0)for(let l=0,c=s.count;l<c;l++)e.isMesh===!0?e.getVertexPosition(l,Si):Si.fromBufferAttribute(s,l),Si.applyMatrix4(e.matrixWorld),this.expandByPoint(Si);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),cc.copy(e.boundingBox)):(n.boundingBox===null&&n.computeBoundingBox(),cc.copy(n.boundingBox)),cc.applyMatrix4(e.matrixWorld),this.union(cc)}const i=e.children;for(let s=0,l=i.length;s<l;s++)this.expandByObject(i[s],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Si),Si.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,n;return e.normal.x>0?(t=e.normal.x*this.min.x,n=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,n=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,n+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,n+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,n+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,n+=e.normal.z*this.min.z),t<=-e.constant&&n>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(oa),uc.subVectors(this.max,oa),no.subVectors(e.a,oa),io.subVectors(e.b,oa),ro.subVectors(e.c,oa),Lr.subVectors(io,no),Dr.subVectors(ro,io),is.subVectors(no,ro);let t=[0,-Lr.z,Lr.y,0,-Dr.z,Dr.y,0,-is.z,is.y,Lr.z,0,-Lr.x,Dr.z,0,-Dr.x,is.z,0,-is.x,-Lr.y,Lr.x,0,-Dr.y,Dr.x,0,-is.y,is.x,0];return!Bf(t,no,io,ro,uc)||(t=[1,0,0,0,1,0,0,0,1],!Bf(t,no,io,ro,uc))?!1:(hc.crossVectors(Lr,Dr),t=[hc.x,hc.y,hc.z],Bf(t,no,io,ro,uc))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Si).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Si).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(rr[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),rr[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),rr[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),rr[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),rr[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),rr[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),rr[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),rr[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(rr),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const rr=[new L,new L,new L,new L,new L,new L,new L,new L],Si=new L,cc=new _n,no=new L,io=new L,ro=new L,Lr=new L,Dr=new L,is=new L,oa=new L,uc=new L,hc=new L,rs=new L;function Bf(r,e,t,n,i){for(let s=0,l=r.length-3;s<=l;s+=3){rs.fromArray(r,s);const c=i.x*Math.abs(rs.x)+i.y*Math.abs(rs.y)+i.z*Math.abs(rs.z),u=e.dot(rs),h=t.dot(rs),f=n.dot(rs);if(Math.max(-Math.max(u,h,f),Math.min(u,h,f))>c)return!1}return!0}const GS=new _n,aa=new L,zf=new L;class yn{constructor(e=new L,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const n=this.center;t!==void 0?n.copy(t):GS.setFromPoints(e).getCenter(n);let i=0;for(let s=0,l=e.length;s<l;s++)i=Math.max(i,n.distanceToSquared(e[s]));return this.radius=Math.sqrt(i),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const n=this.center.distanceToSquared(e);return t.copy(e),n>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;aa.subVectors(e,this.center);const t=aa.lengthSq();if(t>this.radius*this.radius){const n=Math.sqrt(t),i=(n-this.radius)*.5;this.center.addScaledVector(aa,i/n),this.radius+=i}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(zf.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(aa.copy(e.center).add(zf)),this.expandByPoint(aa.copy(e.center).sub(zf))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const sr=new L,kf=new L,fc=new L,Ur=new L,Hf=new L,dc=new L,Vf=new L;class Os{constructor(e=new L,t=new L(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,sr)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const n=t.dot(this.direction);return n<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,n)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=sr.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(sr.copy(this.origin).addScaledVector(this.direction,t),sr.distanceToSquared(e))}distanceSqToSegment(e,t,n,i){kf.copy(e).add(t).multiplyScalar(.5),fc.copy(t).sub(e).normalize(),Ur.copy(this.origin).sub(kf);const s=e.distanceTo(t)*.5,l=-this.direction.dot(fc),c=Ur.dot(this.direction),u=-Ur.dot(fc),h=Ur.lengthSq(),f=Math.abs(1-l*l);let p,m,g,y;if(f>0)if(p=l*u-c,m=l*c-u,y=s*f,p>=0)if(m>=-y)if(m<=y){const M=1/f;p*=M,m*=M,g=p*(p+l*m+2*c)+m*(l*p+m+2*u)+h}else m=s,p=Math.max(0,-(l*m+c)),g=-p*p+m*(m+2*u)+h;else m=-s,p=Math.max(0,-(l*m+c)),g=-p*p+m*(m+2*u)+h;else m<=-y?(p=Math.max(0,-(-l*s+c)),m=p>0?-s:Math.min(Math.max(-s,-u),s),g=-p*p+m*(m+2*u)+h):m<=y?(p=0,m=Math.min(Math.max(-s,-u),s),g=m*(m+2*u)+h):(p=Math.max(0,-(l*s+c)),m=p>0?s:Math.min(Math.max(-s,-u),s),g=-p*p+m*(m+2*u)+h);else m=l>0?-s:s,p=Math.max(0,-(l*m+c)),g=-p*p+m*(m+2*u)+h;return n&&n.copy(this.origin).addScaledVector(this.direction,p),i&&i.copy(kf).addScaledVector(fc,m),g}intersectSphere(e,t){sr.subVectors(e.center,this.origin);const n=sr.dot(this.direction),i=sr.dot(sr)-n*n,s=e.radius*e.radius;if(i>s)return null;const l=Math.sqrt(s-i),c=n-l,u=n+l;return u<0?null:c<0?this.at(u,t):this.at(c,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const n=-(this.origin.dot(e.normal)+e.constant)/t;return n>=0?n:null}intersectPlane(e,t){const n=this.distanceToPlane(e);return n===null?null:this.at(n,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let n,i,s,l,c,u;const h=1/this.direction.x,f=1/this.direction.y,p=1/this.direction.z,m=this.origin;return h>=0?(n=(e.min.x-m.x)*h,i=(e.max.x-m.x)*h):(n=(e.max.x-m.x)*h,i=(e.min.x-m.x)*h),f>=0?(s=(e.min.y-m.y)*f,l=(e.max.y-m.y)*f):(s=(e.max.y-m.y)*f,l=(e.min.y-m.y)*f),n>l||s>i||((s>n||isNaN(n))&&(n=s),(l<i||isNaN(i))&&(i=l),p>=0?(c=(e.min.z-m.z)*p,u=(e.max.z-m.z)*p):(c=(e.max.z-m.z)*p,u=(e.min.z-m.z)*p),n>u||c>i)||((c>n||n!==n)&&(n=c),(u<i||i!==i)&&(i=u),i<0)?null:this.at(n>=0?n:i,t)}intersectsBox(e){return this.intersectBox(e,sr)!==null}intersectTriangle(e,t,n,i,s){Hf.subVectors(t,e),dc.subVectors(n,e),Vf.crossVectors(Hf,dc);let l=this.direction.dot(Vf),c;if(l>0){if(i)return null;c=1}else if(l<0)c=-1,l=-l;else return null;Ur.subVectors(this.origin,e);const u=c*this.direction.dot(dc.crossVectors(Ur,dc));if(u<0)return null;const h=c*this.direction.dot(Hf.cross(Ur));if(h<0||u+h>l)return null;const f=-c*Ur.dot(Vf);return f<0?null:this.at(f/l,s)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class ut{constructor(e,t,n,i,s,l,c,u,h,f,p,m,g,y,M,x){ut.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,n,i,s,l,c,u,h,f,p,m,g,y,M,x)}set(e,t,n,i,s,l,c,u,h,f,p,m,g,y,M,x){const _=this.elements;return _[0]=e,_[4]=t,_[8]=n,_[12]=i,_[1]=s,_[5]=l,_[9]=c,_[13]=u,_[2]=h,_[6]=f,_[10]=p,_[14]=m,_[3]=g,_[7]=y,_[11]=M,_[15]=x,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new ut().fromArray(this.elements)}copy(e){const t=this.elements,n=e.elements;return t[0]=n[0],t[1]=n[1],t[2]=n[2],t[3]=n[3],t[4]=n[4],t[5]=n[5],t[6]=n[6],t[7]=n[7],t[8]=n[8],t[9]=n[9],t[10]=n[10],t[11]=n[11],t[12]=n[12],t[13]=n[13],t[14]=n[14],t[15]=n[15],this}copyPosition(e){const t=this.elements,n=e.elements;return t[12]=n[12],t[13]=n[13],t[14]=n[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,n){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),n.setFromMatrixColumn(this,2),this}makeBasis(e,t,n){return this.set(e.x,t.x,n.x,0,e.y,t.y,n.y,0,e.z,t.z,n.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,n=e.elements,i=1/so.setFromMatrixColumn(e,0).length(),s=1/so.setFromMatrixColumn(e,1).length(),l=1/so.setFromMatrixColumn(e,2).length();return t[0]=n[0]*i,t[1]=n[1]*i,t[2]=n[2]*i,t[3]=0,t[4]=n[4]*s,t[5]=n[5]*s,t[6]=n[6]*s,t[7]=0,t[8]=n[8]*l,t[9]=n[9]*l,t[10]=n[10]*l,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,n=e.x,i=e.y,s=e.z,l=Math.cos(n),c=Math.sin(n),u=Math.cos(i),h=Math.sin(i),f=Math.cos(s),p=Math.sin(s);if(e.order==="XYZ"){const m=l*f,g=l*p,y=c*f,M=c*p;t[0]=u*f,t[4]=-u*p,t[8]=h,t[1]=g+y*h,t[5]=m-M*h,t[9]=-c*u,t[2]=M-m*h,t[6]=y+g*h,t[10]=l*u}else if(e.order==="YXZ"){const m=u*f,g=u*p,y=h*f,M=h*p;t[0]=m+M*c,t[4]=y*c-g,t[8]=l*h,t[1]=l*p,t[5]=l*f,t[9]=-c,t[2]=g*c-y,t[6]=M+m*c,t[10]=l*u}else if(e.order==="ZXY"){const m=u*f,g=u*p,y=h*f,M=h*p;t[0]=m-M*c,t[4]=-l*p,t[8]=y+g*c,t[1]=g+y*c,t[5]=l*f,t[9]=M-m*c,t[2]=-l*h,t[6]=c,t[10]=l*u}else if(e.order==="ZYX"){const m=l*f,g=l*p,y=c*f,M=c*p;t[0]=u*f,t[4]=y*h-g,t[8]=m*h+M,t[1]=u*p,t[5]=M*h+m,t[9]=g*h-y,t[2]=-h,t[6]=c*u,t[10]=l*u}else if(e.order==="YZX"){const m=l*u,g=l*h,y=c*u,M=c*h;t[0]=u*f,t[4]=M-m*p,t[8]=y*p+g,t[1]=p,t[5]=l*f,t[9]=-c*f,t[2]=-h*f,t[6]=g*p+y,t[10]=m-M*p}else if(e.order==="XZY"){const m=l*u,g=l*h,y=c*u,M=c*h;t[0]=u*f,t[4]=-p,t[8]=h*f,t[1]=m*p+M,t[5]=l*f,t[9]=g*p-y,t[2]=y*p-g,t[6]=c*f,t[10]=M*p+m}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(WS,e,XS)}lookAt(e,t,n){const i=this.elements;return ii.subVectors(e,t),ii.lengthSq()===0&&(ii.z=1),ii.normalize(),Nr.crossVectors(n,ii),Nr.lengthSq()===0&&(Math.abs(n.z)===1?ii.x+=1e-4:ii.z+=1e-4,ii.normalize(),Nr.crossVectors(n,ii)),Nr.normalize(),pc.crossVectors(ii,Nr),i[0]=Nr.x,i[4]=pc.x,i[8]=ii.x,i[1]=Nr.y,i[5]=pc.y,i[9]=ii.y,i[2]=Nr.z,i[6]=pc.z,i[10]=ii.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const n=e.elements,i=t.elements,s=this.elements,l=n[0],c=n[4],u=n[8],h=n[12],f=n[1],p=n[5],m=n[9],g=n[13],y=n[2],M=n[6],x=n[10],_=n[14],w=n[3],E=n[7],T=n[11],U=n[15],P=i[0],D=i[4],F=i[8],C=i[12],b=i[1],N=i[5],q=i[9],Y=i[13],K=i[2],le=i[6],$=i[10],pe=i[14],J=i[3],xe=i[7],me=i[11],Se=i[15];return s[0]=l*P+c*b+u*K+h*J,s[4]=l*D+c*N+u*le+h*xe,s[8]=l*F+c*q+u*$+h*me,s[12]=l*C+c*Y+u*pe+h*Se,s[1]=f*P+p*b+m*K+g*J,s[5]=f*D+p*N+m*le+g*xe,s[9]=f*F+p*q+m*$+g*me,s[13]=f*C+p*Y+m*pe+g*Se,s[2]=y*P+M*b+x*K+_*J,s[6]=y*D+M*N+x*le+_*xe,s[10]=y*F+M*q+x*$+_*me,s[14]=y*C+M*Y+x*pe+_*Se,s[3]=w*P+E*b+T*K+U*J,s[7]=w*D+E*N+T*le+U*xe,s[11]=w*F+E*q+T*$+U*me,s[15]=w*C+E*Y+T*pe+U*Se,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],n=e[4],i=e[8],s=e[12],l=e[1],c=e[5],u=e[9],h=e[13],f=e[2],p=e[6],m=e[10],g=e[14],y=e[3],M=e[7],x=e[11],_=e[15];return y*(+s*u*p-i*h*p-s*c*m+n*h*m+i*c*g-n*u*g)+M*(+t*u*g-t*h*m+s*l*m-i*l*g+i*h*f-s*u*f)+x*(+t*h*p-t*c*g-s*l*p+n*l*g+s*c*f-n*h*f)+_*(-i*c*f-t*u*p+t*c*m+i*l*p-n*l*m+n*u*f)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,n){const i=this.elements;return e.isVector3?(i[12]=e.x,i[13]=e.y,i[14]=e.z):(i[12]=e,i[13]=t,i[14]=n),this}invert(){const e=this.elements,t=e[0],n=e[1],i=e[2],s=e[3],l=e[4],c=e[5],u=e[6],h=e[7],f=e[8],p=e[9],m=e[10],g=e[11],y=e[12],M=e[13],x=e[14],_=e[15],w=p*x*h-M*m*h+M*u*g-c*x*g-p*u*_+c*m*_,E=y*m*h-f*x*h-y*u*g+l*x*g+f*u*_-l*m*_,T=f*M*h-y*p*h+y*c*g-l*M*g-f*c*_+l*p*_,U=y*p*u-f*M*u-y*c*m+l*M*m+f*c*x-l*p*x,P=t*w+n*E+i*T+s*U;if(P===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const D=1/P;return e[0]=w*D,e[1]=(M*m*s-p*x*s-M*i*g+n*x*g+p*i*_-n*m*_)*D,e[2]=(c*x*s-M*u*s+M*i*h-n*x*h-c*i*_+n*u*_)*D,e[3]=(p*u*s-c*m*s-p*i*h+n*m*h+c*i*g-n*u*g)*D,e[4]=E*D,e[5]=(f*x*s-y*m*s+y*i*g-t*x*g-f*i*_+t*m*_)*D,e[6]=(y*u*s-l*x*s-y*i*h+t*x*h+l*i*_-t*u*_)*D,e[7]=(l*m*s-f*u*s+f*i*h-t*m*h-l*i*g+t*u*g)*D,e[8]=T*D,e[9]=(y*p*s-f*M*s-y*n*g+t*M*g+f*n*_-t*p*_)*D,e[10]=(l*M*s-y*c*s+y*n*h-t*M*h-l*n*_+t*c*_)*D,e[11]=(f*c*s-l*p*s-f*n*h+t*p*h+l*n*g-t*c*g)*D,e[12]=U*D,e[13]=(f*M*i-y*p*i+y*n*m-t*M*m-f*n*x+t*p*x)*D,e[14]=(y*c*i-l*M*i-y*n*u+t*M*u+l*n*x-t*c*x)*D,e[15]=(l*p*i-f*c*i+f*n*u-t*p*u-l*n*m+t*c*m)*D,this}scale(e){const t=this.elements,n=e.x,i=e.y,s=e.z;return t[0]*=n,t[4]*=i,t[8]*=s,t[1]*=n,t[5]*=i,t[9]*=s,t[2]*=n,t[6]*=i,t[10]*=s,t[3]*=n,t[7]*=i,t[11]*=s,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],n=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],i=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,n,i))}makeTranslation(e,t,n){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,n,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),n=Math.sin(e);return this.set(1,0,0,0,0,t,-n,0,0,n,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),n=Math.sin(e);return this.set(t,0,n,0,0,1,0,0,-n,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),n=Math.sin(e);return this.set(t,-n,0,0,n,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const n=Math.cos(t),i=Math.sin(t),s=1-n,l=e.x,c=e.y,u=e.z,h=s*l,f=s*c;return this.set(h*l+n,h*c-i*u,h*u+i*c,0,h*c+i*u,f*c+n,f*u-i*l,0,h*u-i*c,f*u+i*l,s*u*u+n,0,0,0,0,1),this}makeScale(e,t,n){return this.set(e,0,0,0,0,t,0,0,0,0,n,0,0,0,0,1),this}makeShear(e,t,n,i,s,l){return this.set(1,n,s,0,e,1,l,0,t,i,1,0,0,0,0,1),this}compose(e,t,n){const i=this.elements,s=t._x,l=t._y,c=t._z,u=t._w,h=s+s,f=l+l,p=c+c,m=s*h,g=s*f,y=s*p,M=l*f,x=l*p,_=c*p,w=u*h,E=u*f,T=u*p,U=n.x,P=n.y,D=n.z;return i[0]=(1-(M+_))*U,i[1]=(g+T)*U,i[2]=(y-E)*U,i[3]=0,i[4]=(g-T)*P,i[5]=(1-(m+_))*P,i[6]=(x+w)*P,i[7]=0,i[8]=(y+E)*D,i[9]=(x-w)*D,i[10]=(1-(m+M))*D,i[11]=0,i[12]=e.x,i[13]=e.y,i[14]=e.z,i[15]=1,this}decompose(e,t,n){const i=this.elements;let s=so.set(i[0],i[1],i[2]).length();const l=so.set(i[4],i[5],i[6]).length(),c=so.set(i[8],i[9],i[10]).length();this.determinant()<0&&(s=-s),e.x=i[12],e.y=i[13],e.z=i[14],Mi.copy(this);const h=1/s,f=1/l,p=1/c;return Mi.elements[0]*=h,Mi.elements[1]*=h,Mi.elements[2]*=h,Mi.elements[4]*=f,Mi.elements[5]*=f,Mi.elements[6]*=f,Mi.elements[8]*=p,Mi.elements[9]*=p,Mi.elements[10]*=p,t.setFromRotationMatrix(Mi),n.x=s,n.y=l,n.z=c,this}makePerspective(e,t,n,i,s,l,c=Yi){const u=this.elements,h=2*s/(t-e),f=2*s/(n-i),p=(t+e)/(t-e),m=(n+i)/(n-i);let g,y;if(c===Yi)g=-(l+s)/(l-s),y=-2*l*s/(l-s);else if(c===ka)g=-l/(l-s),y=-l*s/(l-s);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+c);return u[0]=h,u[4]=0,u[8]=p,u[12]=0,u[1]=0,u[5]=f,u[9]=m,u[13]=0,u[2]=0,u[6]=0,u[10]=g,u[14]=y,u[3]=0,u[7]=0,u[11]=-1,u[15]=0,this}makeOrthographic(e,t,n,i,s,l,c=Yi){const u=this.elements,h=1/(t-e),f=1/(n-i),p=1/(l-s),m=(t+e)*h,g=(n+i)*f;let y,M;if(c===Yi)y=(l+s)*p,M=-2*p;else if(c===ka)y=s*p,M=-1*p;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+c);return u[0]=2*h,u[4]=0,u[8]=0,u[12]=-m,u[1]=0,u[5]=2*f,u[9]=0,u[13]=-g,u[2]=0,u[6]=0,u[10]=M,u[14]=-y,u[3]=0,u[7]=0,u[11]=0,u[15]=1,this}equals(e){const t=this.elements,n=e.elements;for(let i=0;i<16;i++)if(t[i]!==n[i])return!1;return!0}fromArray(e,t=0){for(let n=0;n<16;n++)this.elements[n]=e[n+t];return this}toArray(e=[],t=0){const n=this.elements;return e[t]=n[0],e[t+1]=n[1],e[t+2]=n[2],e[t+3]=n[3],e[t+4]=n[4],e[t+5]=n[5],e[t+6]=n[6],e[t+7]=n[7],e[t+8]=n[8],e[t+9]=n[9],e[t+10]=n[10],e[t+11]=n[11],e[t+12]=n[12],e[t+13]=n[13],e[t+14]=n[14],e[t+15]=n[15],e}}const so=new L,Mi=new ut,WS=new L(0,0,0),XS=new L(1,1,1),Nr=new L,pc=new L,ii=new L,Ng=new ut,Og=new Un;class ai{constructor(e=0,t=0,n=0,i=ai.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=n,this._order=i}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,n,i=this._order){return this._x=e,this._y=t,this._z=n,this._order=i,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,n=!0){const i=e.elements,s=i[0],l=i[4],c=i[8],u=i[1],h=i[5],f=i[9],p=i[2],m=i[6],g=i[10];switch(t){case"XYZ":this._y=Math.asin(Jt(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-f,g),this._z=Math.atan2(-l,s)):(this._x=Math.atan2(m,h),this._z=0);break;case"YXZ":this._x=Math.asin(-Jt(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(c,g),this._z=Math.atan2(u,h)):(this._y=Math.atan2(-p,s),this._z=0);break;case"ZXY":this._x=Math.asin(Jt(m,-1,1)),Math.abs(m)<.9999999?(this._y=Math.atan2(-p,g),this._z=Math.atan2(-l,h)):(this._y=0,this._z=Math.atan2(u,s));break;case"ZYX":this._y=Math.asin(-Jt(p,-1,1)),Math.abs(p)<.9999999?(this._x=Math.atan2(m,g),this._z=Math.atan2(u,s)):(this._x=0,this._z=Math.atan2(-l,h));break;case"YZX":this._z=Math.asin(Jt(u,-1,1)),Math.abs(u)<.9999999?(this._x=Math.atan2(-f,h),this._y=Math.atan2(-p,s)):(this._x=0,this._y=Math.atan2(c,g));break;case"XZY":this._z=Math.asin(-Jt(l,-1,1)),Math.abs(l)<.9999999?(this._x=Math.atan2(m,h),this._y=Math.atan2(c,s)):(this._x=Math.atan2(-f,g),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,n===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,n){return Ng.makeRotationFromQuaternion(e),this.setFromRotationMatrix(Ng,t,n)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return Og.setFromEuler(this),this.setFromQuaternion(Og,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}ai.DEFAULT_ORDER="XYZ";class Cs{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let YS=0;const Fg=new L,oo=new Un,or=new ut,mc=new L,la=new L,qS=new L,ZS=new Un,Bg=new L(1,0,0),zg=new L(0,1,0),kg=new L(0,0,1),Hg={type:"added"},jS={type:"removed"},ao={type:"childadded",child:null},Gf={type:"childremoved",child:null};class Dt extends Ji{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:YS++}),this.uuid=oi(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Dt.DEFAULT_UP.clone();const e=new L,t=new ai,n=new Un,i=new L(1,1,1);function s(){n.setFromEuler(t,!1)}function l(){t.setFromQuaternion(n,void 0,!1)}t._onChange(s),n._onChange(l),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:n},scale:{configurable:!0,enumerable:!0,value:i},modelViewMatrix:{value:new ut},normalMatrix:{value:new gt}}),this.matrix=new ut,this.matrixWorld=new ut,this.matrixAutoUpdate=Dt.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Dt.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Cs,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return oo.setFromAxisAngle(e,t),this.quaternion.multiply(oo),this}rotateOnWorldAxis(e,t){return oo.setFromAxisAngle(e,t),this.quaternion.premultiply(oo),this}rotateX(e){return this.rotateOnAxis(Bg,e)}rotateY(e){return this.rotateOnAxis(zg,e)}rotateZ(e){return this.rotateOnAxis(kg,e)}translateOnAxis(e,t){return Fg.copy(e).applyQuaternion(this.quaternion),this.position.add(Fg.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(Bg,e)}translateY(e){return this.translateOnAxis(zg,e)}translateZ(e){return this.translateOnAxis(kg,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(or.copy(this.matrixWorld).invert())}lookAt(e,t,n){e.isVector3?mc.copy(e):mc.set(e,t,n);const i=this.parent;this.updateWorldMatrix(!0,!1),la.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?or.lookAt(la,mc,this.up):or.lookAt(mc,la,this.up),this.quaternion.setFromRotationMatrix(or),i&&(or.extractRotation(i.matrixWorld),oo.setFromRotationMatrix(or),this.quaternion.premultiply(oo.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Hg),ao.child=e,this.dispatchEvent(ao),ao.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let n=0;n<arguments.length;n++)this.remove(arguments[n]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(jS),Gf.child=e,this.dispatchEvent(Gf),Gf.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),or.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),or.multiply(e.parent.matrixWorld)),e.applyMatrix4(or),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Hg),ao.child=e,this.dispatchEvent(ao),ao.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let n=0,i=this.children.length;n<i;n++){const l=this.children[n].getObjectByProperty(e,t);if(l!==void 0)return l}}getObjectsByProperty(e,t,n=[]){this[e]===t&&n.push(this);const i=this.children;for(let s=0,l=i.length;s<l;s++)i[s].getObjectsByProperty(e,t,n);return n}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(la,e,qS),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(la,ZS,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let n=0,i=t.length;n<i;n++)t[n].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let n=0,i=t.length;n<i;n++)t[n].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let n=0,i=t.length;n<i;n++)t[n].updateMatrixWorld(e)}updateWorldMatrix(e,t){const n=this.parent;if(e===!0&&n!==null&&n.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const i=this.children;for(let s=0,l=i.length;s<l;s++)i[s].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",n={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},n.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const i={};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.castShadow===!0&&(i.castShadow=!0),this.receiveShadow===!0&&(i.receiveShadow=!0),this.visible===!1&&(i.visible=!1),this.frustumCulled===!1&&(i.frustumCulled=!1),this.renderOrder!==0&&(i.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(i.userData=this.userData),i.layers=this.layers.mask,i.matrix=this.matrix.toArray(),i.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(i.matrixAutoUpdate=!1),this.isInstancedMesh&&(i.type="InstancedMesh",i.count=this.count,i.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(i.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(i.type="BatchedMesh",i.perObjectFrustumCulled=this.perObjectFrustumCulled,i.sortObjects=this.sortObjects,i.drawRanges=this._drawRanges,i.reservedRanges=this._reservedRanges,i.visibility=this._visibility,i.active=this._active,i.bounds=this._bounds.map(c=>({boxInitialized:c.boxInitialized,boxMin:c.box.min.toArray(),boxMax:c.box.max.toArray(),sphereInitialized:c.sphereInitialized,sphereRadius:c.sphere.radius,sphereCenter:c.sphere.center.toArray()})),i.maxInstanceCount=this._maxInstanceCount,i.maxVertexCount=this._maxVertexCount,i.maxIndexCount=this._maxIndexCount,i.geometryInitialized=this._geometryInitialized,i.geometryCount=this._geometryCount,i.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(i.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(i.boundingSphere={center:i.boundingSphere.center.toArray(),radius:i.boundingSphere.radius}),this.boundingBox!==null&&(i.boundingBox={min:i.boundingBox.min.toArray(),max:i.boundingBox.max.toArray()}));function s(c,u){return c[u.uuid]===void 0&&(c[u.uuid]=u.toJSON(e)),u.uuid}if(this.isScene)this.background&&(this.background.isColor?i.background=this.background.toJSON():this.background.isTexture&&(i.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(i.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){i.geometry=s(e.geometries,this.geometry);const c=this.geometry.parameters;if(c!==void 0&&c.shapes!==void 0){const u=c.shapes;if(Array.isArray(u))for(let h=0,f=u.length;h<f;h++){const p=u[h];s(e.shapes,p)}else s(e.shapes,u)}}if(this.isSkinnedMesh&&(i.bindMode=this.bindMode,i.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(s(e.skeletons,this.skeleton),i.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const c=[];for(let u=0,h=this.material.length;u<h;u++)c.push(s(e.materials,this.material[u]));i.material=c}else i.material=s(e.materials,this.material);if(this.children.length>0){i.children=[];for(let c=0;c<this.children.length;c++)i.children.push(this.children[c].toJSON(e).object)}if(this.animations.length>0){i.animations=[];for(let c=0;c<this.animations.length;c++){const u=this.animations[c];i.animations.push(s(e.animations,u))}}if(t){const c=l(e.geometries),u=l(e.materials),h=l(e.textures),f=l(e.images),p=l(e.shapes),m=l(e.skeletons),g=l(e.animations),y=l(e.nodes);c.length>0&&(n.geometries=c),u.length>0&&(n.materials=u),h.length>0&&(n.textures=h),f.length>0&&(n.images=f),p.length>0&&(n.shapes=p),m.length>0&&(n.skeletons=m),g.length>0&&(n.animations=g),y.length>0&&(n.nodes=y)}return n.object=i,n;function l(c){const u=[];for(const h in c){const f=c[h];delete f.metadata,u.push(f)}return u}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let n=0;n<e.children.length;n++){const i=e.children[n];this.add(i.clone())}return this}}Dt.DEFAULT_UP=new L(0,1,0);Dt.DEFAULT_MATRIX_AUTO_UPDATE=!0;Dt.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Ei=new L,ar=new L,Wf=new L,lr=new L,lo=new L,co=new L,Vg=new L,Xf=new L,Yf=new L,qf=new L,Zf=new At,jf=new At,Jf=new At;class Jn{constructor(e=new L,t=new L,n=new L){this.a=e,this.b=t,this.c=n}static getNormal(e,t,n,i){i.subVectors(n,t),Ei.subVectors(e,t),i.cross(Ei);const s=i.lengthSq();return s>0?i.multiplyScalar(1/Math.sqrt(s)):i.set(0,0,0)}static getBarycoord(e,t,n,i,s){Ei.subVectors(i,t),ar.subVectors(n,t),Wf.subVectors(e,t);const l=Ei.dot(Ei),c=Ei.dot(ar),u=Ei.dot(Wf),h=ar.dot(ar),f=ar.dot(Wf),p=l*h-c*c;if(p===0)return s.set(0,0,0),null;const m=1/p,g=(h*u-c*f)*m,y=(l*f-c*u)*m;return s.set(1-g-y,y,g)}static containsPoint(e,t,n,i){return this.getBarycoord(e,t,n,i,lr)===null?!1:lr.x>=0&&lr.y>=0&&lr.x+lr.y<=1}static getInterpolation(e,t,n,i,s,l,c,u){return this.getBarycoord(e,t,n,i,lr)===null?(u.x=0,u.y=0,"z"in u&&(u.z=0),"w"in u&&(u.w=0),null):(u.setScalar(0),u.addScaledVector(s,lr.x),u.addScaledVector(l,lr.y),u.addScaledVector(c,lr.z),u)}static getInterpolatedAttribute(e,t,n,i,s,l){return Zf.setScalar(0),jf.setScalar(0),Jf.setScalar(0),Zf.fromBufferAttribute(e,t),jf.fromBufferAttribute(e,n),Jf.fromBufferAttribute(e,i),l.setScalar(0),l.addScaledVector(Zf,s.x),l.addScaledVector(jf,s.y),l.addScaledVector(Jf,s.z),l}static isFrontFacing(e,t,n,i){return Ei.subVectors(n,t),ar.subVectors(e,t),Ei.cross(ar).dot(i)<0}set(e,t,n){return this.a.copy(e),this.b.copy(t),this.c.copy(n),this}setFromPointsAndIndices(e,t,n,i){return this.a.copy(e[t]),this.b.copy(e[n]),this.c.copy(e[i]),this}setFromAttributeAndIndices(e,t,n,i){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,n),this.c.fromBufferAttribute(e,i),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Ei.subVectors(this.c,this.b),ar.subVectors(this.a,this.b),Ei.cross(ar).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Jn.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Jn.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,n,i,s){return Jn.getInterpolation(e,this.a,this.b,this.c,t,n,i,s)}containsPoint(e){return Jn.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Jn.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const n=this.a,i=this.b,s=this.c;let l,c;lo.subVectors(i,n),co.subVectors(s,n),Xf.subVectors(e,n);const u=lo.dot(Xf),h=co.dot(Xf);if(u<=0&&h<=0)return t.copy(n);Yf.subVectors(e,i);const f=lo.dot(Yf),p=co.dot(Yf);if(f>=0&&p<=f)return t.copy(i);const m=u*p-f*h;if(m<=0&&u>=0&&f<=0)return l=u/(u-f),t.copy(n).addScaledVector(lo,l);qf.subVectors(e,s);const g=lo.dot(qf),y=co.dot(qf);if(y>=0&&g<=y)return t.copy(s);const M=g*h-u*y;if(M<=0&&h>=0&&y<=0)return c=h/(h-y),t.copy(n).addScaledVector(co,c);const x=f*y-g*p;if(x<=0&&p-f>=0&&g-y>=0)return Vg.subVectors(s,i),c=(p-f)/(p-f+(g-y)),t.copy(i).addScaledVector(Vg,c);const _=1/(x+M+m);return l=M*_,c=m*_,t.copy(n).addScaledVector(lo,l).addScaledVector(co,c)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const E_={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Or={h:0,s:0,l:0},gc={h:0,s:0,l:0};function Kf(r,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?r+(e-r)*6*t:t<1/2?e:t<2/3?r+(e-r)*6*(2/3-t):r}class Be{constructor(e,t,n){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,n)}set(e,t,n){if(t===void 0&&n===void 0){const i=e;i&&i.isColor?this.copy(i):typeof i=="number"?this.setHex(i):typeof i=="string"&&this.setStyle(i)}else this.setRGB(e,t,n);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=jn){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Pt.toWorkingColorSpace(this,t),this}setRGB(e,t,n,i=Pt.workingColorSpace){return this.r=e,this.g=t,this.b=n,Pt.toWorkingColorSpace(this,i),this}setHSL(e,t,n,i=Pt.workingColorSpace){if(e=pp(e,1),t=Jt(t,0,1),n=Jt(n,0,1),t===0)this.r=this.g=this.b=n;else{const s=n<=.5?n*(1+t):n+t-n*t,l=2*n-s;this.r=Kf(l,s,e+1/3),this.g=Kf(l,s,e),this.b=Kf(l,s,e-1/3)}return Pt.toWorkingColorSpace(this,i),this}setStyle(e,t=jn){function n(s){s!==void 0&&parseFloat(s)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let i;if(i=/^(\w+)\(([^\)]*)\)/.exec(e)){let s;const l=i[1],c=i[2];switch(l){case"rgb":case"rgba":if(s=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return n(s[4]),this.setRGB(Math.min(255,parseInt(s[1],10))/255,Math.min(255,parseInt(s[2],10))/255,Math.min(255,parseInt(s[3],10))/255,t);if(s=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return n(s[4]),this.setRGB(Math.min(100,parseInt(s[1],10))/100,Math.min(100,parseInt(s[2],10))/100,Math.min(100,parseInt(s[3],10))/100,t);break;case"hsl":case"hsla":if(s=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return n(s[4]),this.setHSL(parseFloat(s[1])/360,parseFloat(s[2])/100,parseFloat(s[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(i=/^\#([A-Fa-f\d]+)$/.exec(e)){const s=i[1],l=s.length;if(l===3)return this.setRGB(parseInt(s.charAt(0),16)/15,parseInt(s.charAt(1),16)/15,parseInt(s.charAt(2),16)/15,t);if(l===6)return this.setHex(parseInt(s,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=jn){const n=E_[e.toLowerCase()];return n!==void 0?this.setHex(n,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=gr(e.r),this.g=gr(e.g),this.b=gr(e.b),this}copyLinearToSRGB(e){return this.r=Po(e.r),this.g=Po(e.g),this.b=Po(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=jn){return Pt.fromWorkingColorSpace(In.copy(this),e),Math.round(Jt(In.r*255,0,255))*65536+Math.round(Jt(In.g*255,0,255))*256+Math.round(Jt(In.b*255,0,255))}getHexString(e=jn){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Pt.workingColorSpace){Pt.fromWorkingColorSpace(In.copy(this),t);const n=In.r,i=In.g,s=In.b,l=Math.max(n,i,s),c=Math.min(n,i,s);let u,h;const f=(c+l)/2;if(c===l)u=0,h=0;else{const p=l-c;switch(h=f<=.5?p/(l+c):p/(2-l-c),l){case n:u=(i-s)/p+(i<s?6:0);break;case i:u=(s-n)/p+2;break;case s:u=(n-i)/p+4;break}u/=6}return e.h=u,e.s=h,e.l=f,e}getRGB(e,t=Pt.workingColorSpace){return Pt.fromWorkingColorSpace(In.copy(this),t),e.r=In.r,e.g=In.g,e.b=In.b,e}getStyle(e=jn){Pt.fromWorkingColorSpace(In.copy(this),e);const t=In.r,n=In.g,i=In.b;return e!==jn?`color(${e} ${t.toFixed(3)} ${n.toFixed(3)} ${i.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(n*255)},${Math.round(i*255)})`}offsetHSL(e,t,n){return this.getHSL(Or),this.setHSL(Or.h+e,Or.s+t,Or.l+n)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,n){return this.r=e.r+(t.r-e.r)*n,this.g=e.g+(t.g-e.g)*n,this.b=e.b+(t.b-e.b)*n,this}lerpHSL(e,t){this.getHSL(Or),e.getHSL(gc);const n=Pa(Or.h,gc.h,t),i=Pa(Or.s,gc.s,t),s=Pa(Or.l,gc.l,t);return this.setHSL(n,i,s),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,n=this.g,i=this.b,s=e.elements;return this.r=s[0]*t+s[3]*n+s[6]*i,this.g=s[1]*t+s[4]*n+s[7]*i,this.b=s[2]*t+s[5]*n+s[8]*i,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const In=new Be;Be.NAMES=E_;let JS=0;class Nn extends Ji{static get type(){return"Material"}get type(){return this.constructor.type}set type(e){}constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:JS++}),this.uuid=oi(),this.name="",this.blending=Ts,this.side=vr,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=cu,this.blendDst=uu,this.blendEquation=zr,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new Be(0,0,0),this.blendAlpha=0,this.depthFunc=Is,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Hd,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=_s,this.stencilZFail=_s,this.stencilZPass=_s,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const n=e[t];if(n===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const i=this[t];if(i===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}i&&i.isColor?i.set(n):i&&i.isVector3&&n&&n.isVector3?i.copy(n):this[t]=n}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const n={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};n.uuid=this.uuid,n.type=this.type,this.name!==""&&(n.name=this.name),this.color&&this.color.isColor&&(n.color=this.color.getHex()),this.roughness!==void 0&&(n.roughness=this.roughness),this.metalness!==void 0&&(n.metalness=this.metalness),this.sheen!==void 0&&(n.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(n.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(n.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(n.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(n.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(n.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(n.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(n.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(n.shininess=this.shininess),this.clearcoat!==void 0&&(n.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(n.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(n.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(n.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(n.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,n.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(n.dispersion=this.dispersion),this.iridescence!==void 0&&(n.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(n.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(n.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(n.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(n.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(n.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(n.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(n.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(n.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(n.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(n.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(n.lightMap=this.lightMap.toJSON(e).uuid,n.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(n.aoMap=this.aoMap.toJSON(e).uuid,n.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(n.bumpMap=this.bumpMap.toJSON(e).uuid,n.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(n.normalMap=this.normalMap.toJSON(e).uuid,n.normalMapType=this.normalMapType,n.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(n.displacementMap=this.displacementMap.toJSON(e).uuid,n.displacementScale=this.displacementScale,n.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(n.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(n.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(n.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(n.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(n.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(n.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(n.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(n.combine=this.combine)),this.envMapRotation!==void 0&&(n.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(n.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(n.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(n.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(n.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(n.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(n.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(n.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(n.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(n.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(n.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(n.size=this.size),this.shadowSide!==null&&(n.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(n.sizeAttenuation=this.sizeAttenuation),this.blending!==Ts&&(n.blending=this.blending),this.side!==vr&&(n.side=this.side),this.vertexColors===!0&&(n.vertexColors=!0),this.opacity<1&&(n.opacity=this.opacity),this.transparent===!0&&(n.transparent=!0),this.blendSrc!==cu&&(n.blendSrc=this.blendSrc),this.blendDst!==uu&&(n.blendDst=this.blendDst),this.blendEquation!==zr&&(n.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(n.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(n.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(n.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(n.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(n.blendAlpha=this.blendAlpha),this.depthFunc!==Is&&(n.depthFunc=this.depthFunc),this.depthTest===!1&&(n.depthTest=this.depthTest),this.depthWrite===!1&&(n.depthWrite=this.depthWrite),this.colorWrite===!1&&(n.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(n.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==Hd&&(n.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(n.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(n.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==_s&&(n.stencilFail=this.stencilFail),this.stencilZFail!==_s&&(n.stencilZFail=this.stencilZFail),this.stencilZPass!==_s&&(n.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(n.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(n.rotation=this.rotation),this.polygonOffset===!0&&(n.polygonOffset=!0),this.polygonOffsetFactor!==0&&(n.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(n.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(n.linewidth=this.linewidth),this.dashSize!==void 0&&(n.dashSize=this.dashSize),this.gapSize!==void 0&&(n.gapSize=this.gapSize),this.scale!==void 0&&(n.scale=this.scale),this.dithering===!0&&(n.dithering=!0),this.alphaTest>0&&(n.alphaTest=this.alphaTest),this.alphaHash===!0&&(n.alphaHash=!0),this.alphaToCoverage===!0&&(n.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(n.premultipliedAlpha=!0),this.forceSinglePass===!0&&(n.forceSinglePass=!0),this.wireframe===!0&&(n.wireframe=!0),this.wireframeLinewidth>1&&(n.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(n.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(n.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(n.flatShading=!0),this.visible===!1&&(n.visible=!1),this.toneMapped===!1&&(n.toneMapped=!1),this.fog===!1&&(n.fog=!1),Object.keys(this.userData).length>0&&(n.userData=this.userData);function i(s){const l=[];for(const c in s){const u=s[c];delete u.metadata,l.push(u)}return l}if(t){const s=i(e.textures),l=i(e.images);s.length>0&&(n.textures=s),l.length>0&&(n.images=l)}return n}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let n=null;if(t!==null){const i=t.length;n=new Array(i);for(let s=0;s!==i;++s)n[s]=t[s].clone()}return this.clippingPlanes=n,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Wr extends Nn{static get type(){return"MeshBasicMaterial"}constructor(e){super(),this.isMeshBasicMaterial=!0,this.color=new Be(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new ai,this.combine=Ka,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const dr=KS();function KS(){const r=new ArrayBuffer(4),e=new Float32Array(r),t=new Uint32Array(r),n=new Uint32Array(512),i=new Uint32Array(512);for(let u=0;u<256;++u){const h=u-127;h<-27?(n[u]=0,n[u|256]=32768,i[u]=24,i[u|256]=24):h<-14?(n[u]=1024>>-h-14,n[u|256]=1024>>-h-14|32768,i[u]=-h-1,i[u|256]=-h-1):h<=15?(n[u]=h+15<<10,n[u|256]=h+15<<10|32768,i[u]=13,i[u|256]=13):h<128?(n[u]=31744,n[u|256]=64512,i[u]=24,i[u|256]=24):(n[u]=31744,n[u|256]=64512,i[u]=13,i[u|256]=13)}const s=new Uint32Array(2048),l=new Uint32Array(64),c=new Uint32Array(64);for(let u=1;u<1024;++u){let h=u<<13,f=0;for(;!(h&8388608);)h<<=1,f-=8388608;h&=-8388609,f+=947912704,s[u]=h|f}for(let u=1024;u<2048;++u)s[u]=939524096+(u-1024<<13);for(let u=1;u<31;++u)l[u]=u<<23;l[31]=1199570944,l[32]=2147483648;for(let u=33;u<63;++u)l[u]=2147483648+(u-32<<23);l[63]=3347054592;for(let u=1;u<64;++u)u!==32&&(c[u]=1024);return{floatView:e,uint32View:t,baseTable:n,shiftTable:i,mantissaTable:s,exponentTable:l,offsetTable:c}}function Zn(r){Math.abs(r)>65504&&console.warn("THREE.DataUtils.toHalfFloat(): Value out of range."),r=Jt(r,-65504,65504),dr.floatView[0]=r;const e=dr.uint32View[0],t=e>>23&511;return dr.baseTable[t]+((e&8388607)>>dr.shiftTable[t])}function Sa(r){const e=r>>10;return dr.uint32View[0]=dr.mantissaTable[dr.offsetTable[e]+(r&1023)]+dr.exponentTable[e],dr.floatView[0]}const QS={toHalfFloat:Zn,fromHalfFloat:Sa},an=new L,vc=new ae;class zt{constructor(e,t,n=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=n,this.usage=za,this.updateRanges=[],this.gpuType=Kn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,n){e*=this.itemSize,n*=t.itemSize;for(let i=0,s=this.itemSize;i<s;i++)this.array[e+i]=t.array[n+i];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,n=this.count;t<n;t++)vc.fromBufferAttribute(this,t),vc.applyMatrix3(e),this.setXY(t,vc.x,vc.y);else if(this.itemSize===3)for(let t=0,n=this.count;t<n;t++)an.fromBufferAttribute(this,t),an.applyMatrix3(e),this.setXYZ(t,an.x,an.y,an.z);return this}applyMatrix4(e){for(let t=0,n=this.count;t<n;t++)an.fromBufferAttribute(this,t),an.applyMatrix4(e),this.setXYZ(t,an.x,an.y,an.z);return this}applyNormalMatrix(e){for(let t=0,n=this.count;t<n;t++)an.fromBufferAttribute(this,t),an.applyNormalMatrix(e),this.setXYZ(t,an.x,an.y,an.z);return this}transformDirection(e){for(let t=0,n=this.count;t<n;t++)an.fromBufferAttribute(this,t),an.transformDirection(e),this.setXYZ(t,an.x,an.y,an.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let n=this.array[e*this.itemSize+t];return this.normalized&&(n=Hn(n,this.array)),n}setComponent(e,t,n){return this.normalized&&(n=vt(n,this.array)),this.array[e*this.itemSize+t]=n,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Hn(t,this.array)),t}setX(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Hn(t,this.array)),t}setY(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Hn(t,this.array)),t}setZ(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Hn(t,this.array)),t}setW(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,n){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array)),this.array[e+0]=t,this.array[e+1]=n,this}setXYZ(e,t,n,i){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array)),this.array[e+0]=t,this.array[e+1]=n,this.array[e+2]=i,this}setXYZW(e,t,n,i,s){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array),s=vt(s,this.array)),this.array[e+0]=t,this.array[e+1]=n,this.array[e+2]=i,this.array[e+3]=s,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==za&&(e.usage=this.usage),e}}class $S extends zt{constructor(e,t,n){super(new Int8Array(e),t,n)}}class eM extends zt{constructor(e,t,n){super(new Uint8Array(e),t,n)}}class tM extends zt{constructor(e,t,n){super(new Uint8ClampedArray(e),t,n)}}class nM extends zt{constructor(e,t,n){super(new Int16Array(e),t,n)}}class gp extends zt{constructor(e,t,n){super(new Uint16Array(e),t,n)}}class iM extends zt{constructor(e,t,n){super(new Int32Array(e),t,n)}}class vp extends zt{constructor(e,t,n){super(new Uint32Array(e),t,n)}}class rM extends zt{constructor(e,t,n){super(new Uint16Array(e),t,n),this.isFloat16BufferAttribute=!0}getX(e){let t=Sa(this.array[e*this.itemSize]);return this.normalized&&(t=Hn(t,this.array)),t}setX(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize]=Zn(t),this}getY(e){let t=Sa(this.array[e*this.itemSize+1]);return this.normalized&&(t=Hn(t,this.array)),t}setY(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+1]=Zn(t),this}getZ(e){let t=Sa(this.array[e*this.itemSize+2]);return this.normalized&&(t=Hn(t,this.array)),t}setZ(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+2]=Zn(t),this}getW(e){let t=Sa(this.array[e*this.itemSize+3]);return this.normalized&&(t=Hn(t,this.array)),t}setW(e,t){return this.normalized&&(t=vt(t,this.array)),this.array[e*this.itemSize+3]=Zn(t),this}setXY(e,t,n){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array)),this.array[e+0]=Zn(t),this.array[e+1]=Zn(n),this}setXYZ(e,t,n,i){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array)),this.array[e+0]=Zn(t),this.array[e+1]=Zn(n),this.array[e+2]=Zn(i),this}setXYZW(e,t,n,i,s){return e*=this.itemSize,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array),s=vt(s,this.array)),this.array[e+0]=Zn(t),this.array[e+1]=Zn(n),this.array[e+2]=Zn(i),this.array[e+3]=Zn(s),this}}class Ye extends zt{constructor(e,t,n){super(new Float32Array(e),t,n)}}let sM=0;const gi=new ut,Qf=new Dt,uo=new L,ri=new _n,ca=new _n,vn=new L;class xt extends Ji{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:sM++}),this.uuid=oi(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(y_(e)?vp:gp)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,n=0){this.groups.push({start:e,count:t,materialIndex:n})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const n=this.attributes.normal;if(n!==void 0){const s=new gt().getNormalMatrix(e);n.applyNormalMatrix(s),n.needsUpdate=!0}const i=this.attributes.tangent;return i!==void 0&&(i.transformDirection(e),i.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return gi.makeRotationFromQuaternion(e),this.applyMatrix4(gi),this}rotateX(e){return gi.makeRotationX(e),this.applyMatrix4(gi),this}rotateY(e){return gi.makeRotationY(e),this.applyMatrix4(gi),this}rotateZ(e){return gi.makeRotationZ(e),this.applyMatrix4(gi),this}translate(e,t,n){return gi.makeTranslation(e,t,n),this.applyMatrix4(gi),this}scale(e,t,n){return gi.makeScale(e,t,n),this.applyMatrix4(gi),this}lookAt(e){return Qf.lookAt(e),Qf.updateMatrix(),this.applyMatrix4(Qf.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(uo).negate(),this.translate(uo.x,uo.y,uo.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const n=[];for(let i=0,s=e.length;i<s;i++){const l=e[i];n.push(l.x,l.y,l.z||0)}this.setAttribute("position",new Ye(n,3))}else{for(let n=0,i=t.count;n<i;n++){const s=e[n];t.setXYZ(n,s.x,s.y,s.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new _n);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new L(-1/0,-1/0,-1/0),new L(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let n=0,i=t.length;n<i;n++){const s=t[n];ri.setFromBufferAttribute(s),this.morphTargetsRelative?(vn.addVectors(this.boundingBox.min,ri.min),this.boundingBox.expandByPoint(vn),vn.addVectors(this.boundingBox.max,ri.max),this.boundingBox.expandByPoint(vn)):(this.boundingBox.expandByPoint(ri.min),this.boundingBox.expandByPoint(ri.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new yn);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new L,1/0);return}if(e){const n=this.boundingSphere.center;if(ri.setFromBufferAttribute(e),t)for(let s=0,l=t.length;s<l;s++){const c=t[s];ca.setFromBufferAttribute(c),this.morphTargetsRelative?(vn.addVectors(ri.min,ca.min),ri.expandByPoint(vn),vn.addVectors(ri.max,ca.max),ri.expandByPoint(vn)):(ri.expandByPoint(ca.min),ri.expandByPoint(ca.max))}ri.getCenter(n);let i=0;for(let s=0,l=e.count;s<l;s++)vn.fromBufferAttribute(e,s),i=Math.max(i,n.distanceToSquared(vn));if(t)for(let s=0,l=t.length;s<l;s++){const c=t[s],u=this.morphTargetsRelative;for(let h=0,f=c.count;h<f;h++)vn.fromBufferAttribute(c,h),u&&(uo.fromBufferAttribute(e,h),vn.add(uo)),i=Math.max(i,n.distanceToSquared(vn))}this.boundingSphere.radius=Math.sqrt(i),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const n=t.position,i=t.normal,s=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new zt(new Float32Array(4*n.count),4));const l=this.getAttribute("tangent"),c=[],u=[];for(let F=0;F<n.count;F++)c[F]=new L,u[F]=new L;const h=new L,f=new L,p=new L,m=new ae,g=new ae,y=new ae,M=new L,x=new L;function _(F,C,b){h.fromBufferAttribute(n,F),f.fromBufferAttribute(n,C),p.fromBufferAttribute(n,b),m.fromBufferAttribute(s,F),g.fromBufferAttribute(s,C),y.fromBufferAttribute(s,b),f.sub(h),p.sub(h),g.sub(m),y.sub(m);const N=1/(g.x*y.y-y.x*g.y);isFinite(N)&&(M.copy(f).multiplyScalar(y.y).addScaledVector(p,-g.y).multiplyScalar(N),x.copy(p).multiplyScalar(g.x).addScaledVector(f,-y.x).multiplyScalar(N),c[F].add(M),c[C].add(M),c[b].add(M),u[F].add(x),u[C].add(x),u[b].add(x))}let w=this.groups;w.length===0&&(w=[{start:0,count:e.count}]);for(let F=0,C=w.length;F<C;++F){const b=w[F],N=b.start,q=b.count;for(let Y=N,K=N+q;Y<K;Y+=3)_(e.getX(Y+0),e.getX(Y+1),e.getX(Y+2))}const E=new L,T=new L,U=new L,P=new L;function D(F){U.fromBufferAttribute(i,F),P.copy(U);const C=c[F];E.copy(C),E.sub(U.multiplyScalar(U.dot(C))).normalize(),T.crossVectors(P,C);const N=T.dot(u[F])<0?-1:1;l.setXYZW(F,E.x,E.y,E.z,N)}for(let F=0,C=w.length;F<C;++F){const b=w[F],N=b.start,q=b.count;for(let Y=N,K=N+q;Y<K;Y+=3)D(e.getX(Y+0)),D(e.getX(Y+1)),D(e.getX(Y+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let n=this.getAttribute("normal");if(n===void 0)n=new zt(new Float32Array(t.count*3),3),this.setAttribute("normal",n);else for(let m=0,g=n.count;m<g;m++)n.setXYZ(m,0,0,0);const i=new L,s=new L,l=new L,c=new L,u=new L,h=new L,f=new L,p=new L;if(e)for(let m=0,g=e.count;m<g;m+=3){const y=e.getX(m+0),M=e.getX(m+1),x=e.getX(m+2);i.fromBufferAttribute(t,y),s.fromBufferAttribute(t,M),l.fromBufferAttribute(t,x),f.subVectors(l,s),p.subVectors(i,s),f.cross(p),c.fromBufferAttribute(n,y),u.fromBufferAttribute(n,M),h.fromBufferAttribute(n,x),c.add(f),u.add(f),h.add(f),n.setXYZ(y,c.x,c.y,c.z),n.setXYZ(M,u.x,u.y,u.z),n.setXYZ(x,h.x,h.y,h.z)}else for(let m=0,g=t.count;m<g;m+=3)i.fromBufferAttribute(t,m+0),s.fromBufferAttribute(t,m+1),l.fromBufferAttribute(t,m+2),f.subVectors(l,s),p.subVectors(i,s),f.cross(p),n.setXYZ(m+0,f.x,f.y,f.z),n.setXYZ(m+1,f.x,f.y,f.z),n.setXYZ(m+2,f.x,f.y,f.z);this.normalizeNormals(),n.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,n=e.count;t<n;t++)vn.fromBufferAttribute(e,t),vn.normalize(),e.setXYZ(t,vn.x,vn.y,vn.z)}toNonIndexed(){function e(c,u){const h=c.array,f=c.itemSize,p=c.normalized,m=new h.constructor(u.length*f);let g=0,y=0;for(let M=0,x=u.length;M<x;M++){c.isInterleavedBufferAttribute?g=u[M]*c.data.stride+c.offset:g=u[M]*f;for(let _=0;_<f;_++)m[y++]=h[g++]}return new zt(m,f,p)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new xt,n=this.index.array,i=this.attributes;for(const c in i){const u=i[c],h=e(u,n);t.setAttribute(c,h)}const s=this.morphAttributes;for(const c in s){const u=[],h=s[c];for(let f=0,p=h.length;f<p;f++){const m=h[f],g=e(m,n);u.push(g)}t.morphAttributes[c]=u}t.morphTargetsRelative=this.morphTargetsRelative;const l=this.groups;for(let c=0,u=l.length;c<u;c++){const h=l[c];t.addGroup(h.start,h.count,h.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const u=this.parameters;for(const h in u)u[h]!==void 0&&(e[h]=u[h]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const n=this.attributes;for(const u in n){const h=n[u];e.data.attributes[u]=h.toJSON(e.data)}const i={};let s=!1;for(const u in this.morphAttributes){const h=this.morphAttributes[u],f=[];for(let p=0,m=h.length;p<m;p++){const g=h[p];f.push(g.toJSON(e.data))}f.length>0&&(i[u]=f,s=!0)}s&&(e.data.morphAttributes=i,e.data.morphTargetsRelative=this.morphTargetsRelative);const l=this.groups;l.length>0&&(e.data.groups=JSON.parse(JSON.stringify(l)));const c=this.boundingSphere;return c!==null&&(e.data.boundingSphere={center:c.center.toArray(),radius:c.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const n=e.index;n!==null&&this.setIndex(n.clone(t));const i=e.attributes;for(const h in i){const f=i[h];this.setAttribute(h,f.clone(t))}const s=e.morphAttributes;for(const h in s){const f=[],p=s[h];for(let m=0,g=p.length;m<g;m++)f.push(p[m].clone(t));this.morphAttributes[h]=f}this.morphTargetsRelative=e.morphTargetsRelative;const l=e.groups;for(let h=0,f=l.length;h<f;h++){const p=l[h];this.addGroup(p.start,p.count,p.materialIndex)}const c=e.boundingBox;c!==null&&(this.boundingBox=c.clone());const u=e.boundingSphere;return u!==null&&(this.boundingSphere=u.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const Gg=new ut,ss=new Os,_c=new yn,Wg=new L,yc=new L,xc=new L,Sc=new L,$f=new L,Mc=new L,Xg=new L,Ec=new L;class nn extends Dt{constructor(e=new xt,t=new Wr){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,n=Object.keys(t);if(n.length>0){const i=t[n[0]];if(i!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,l=i.length;s<l;s++){const c=i[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}getVertexPosition(e,t){const n=this.geometry,i=n.attributes.position,s=n.morphAttributes.position,l=n.morphTargetsRelative;t.fromBufferAttribute(i,e);const c=this.morphTargetInfluences;if(s&&c){Mc.set(0,0,0);for(let u=0,h=s.length;u<h;u++){const f=c[u],p=s[u];f!==0&&($f.fromBufferAttribute(p,e),l?Mc.addScaledVector($f,f):Mc.addScaledVector($f.sub(t),f))}t.add(Mc)}return t}raycast(e,t){const n=this.geometry,i=this.material,s=this.matrixWorld;i!==void 0&&(n.boundingSphere===null&&n.computeBoundingSphere(),_c.copy(n.boundingSphere),_c.applyMatrix4(s),ss.copy(e.ray).recast(e.near),!(_c.containsPoint(ss.origin)===!1&&(ss.intersectSphere(_c,Wg)===null||ss.origin.distanceToSquared(Wg)>(e.far-e.near)**2))&&(Gg.copy(s).invert(),ss.copy(e.ray).applyMatrix4(Gg),!(n.boundingBox!==null&&ss.intersectsBox(n.boundingBox)===!1)&&this._computeIntersections(e,t,ss)))}_computeIntersections(e,t,n){let i;const s=this.geometry,l=this.material,c=s.index,u=s.attributes.position,h=s.attributes.uv,f=s.attributes.uv1,p=s.attributes.normal,m=s.groups,g=s.drawRange;if(c!==null)if(Array.isArray(l))for(let y=0,M=m.length;y<M;y++){const x=m[y],_=l[x.materialIndex],w=Math.max(x.start,g.start),E=Math.min(c.count,Math.min(x.start+x.count,g.start+g.count));for(let T=w,U=E;T<U;T+=3){const P=c.getX(T),D=c.getX(T+1),F=c.getX(T+2);i=wc(this,_,e,n,h,f,p,P,D,F),i&&(i.faceIndex=Math.floor(T/3),i.face.materialIndex=x.materialIndex,t.push(i))}}else{const y=Math.max(0,g.start),M=Math.min(c.count,g.start+g.count);for(let x=y,_=M;x<_;x+=3){const w=c.getX(x),E=c.getX(x+1),T=c.getX(x+2);i=wc(this,l,e,n,h,f,p,w,E,T),i&&(i.faceIndex=Math.floor(x/3),t.push(i))}}else if(u!==void 0)if(Array.isArray(l))for(let y=0,M=m.length;y<M;y++){const x=m[y],_=l[x.materialIndex],w=Math.max(x.start,g.start),E=Math.min(u.count,Math.min(x.start+x.count,g.start+g.count));for(let T=w,U=E;T<U;T+=3){const P=T,D=T+1,F=T+2;i=wc(this,_,e,n,h,f,p,P,D,F),i&&(i.faceIndex=Math.floor(T/3),i.face.materialIndex=x.materialIndex,t.push(i))}}else{const y=Math.max(0,g.start),M=Math.min(u.count,g.start+g.count);for(let x=y,_=M;x<_;x+=3){const w=x,E=x+1,T=x+2;i=wc(this,l,e,n,h,f,p,w,E,T),i&&(i.faceIndex=Math.floor(x/3),t.push(i))}}}}function oM(r,e,t,n,i,s,l,c){let u;if(e.side===Vn?u=n.intersectTriangle(l,s,i,!0,c):u=n.intersectTriangle(i,s,l,e.side===vr,c),u===null)return null;Ec.copy(c),Ec.applyMatrix4(r.matrixWorld);const h=t.ray.origin.distanceTo(Ec);return h<t.near||h>t.far?null:{distance:h,point:Ec.clone(),object:r}}function wc(r,e,t,n,i,s,l,c,u,h){r.getVertexPosition(c,yc),r.getVertexPosition(u,xc),r.getVertexPosition(h,Sc);const f=oM(r,e,t,n,yc,xc,Sc,Xg);if(f){const p=new L;Jn.getBarycoord(Xg,yc,xc,Sc,p),i&&(f.uv=Jn.getInterpolatedAttribute(i,c,u,h,p,new ae)),s&&(f.uv1=Jn.getInterpolatedAttribute(s,c,u,h,p,new ae)),l&&(f.normal=Jn.getInterpolatedAttribute(l,c,u,h,p,new L),f.normal.dot(n.direction)>0&&f.normal.multiplyScalar(-1));const m={a:c,b:u,c:h,normal:new L,materialIndex:0};Jn.getNormal(yc,xc,Sc,m.normal),f.face=m,f.barycoord=p}return f}class Fs extends xt{constructor(e=1,t=1,n=1,i=1,s=1,l=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:n,widthSegments:i,heightSegments:s,depthSegments:l};const c=this;i=Math.floor(i),s=Math.floor(s),l=Math.floor(l);const u=[],h=[],f=[],p=[];let m=0,g=0;y("z","y","x",-1,-1,n,t,e,l,s,0),y("z","y","x",1,-1,n,t,-e,l,s,1),y("x","z","y",1,1,e,n,t,i,l,2),y("x","z","y",1,-1,e,n,-t,i,l,3),y("x","y","z",1,-1,e,t,n,i,s,4),y("x","y","z",-1,-1,e,t,-n,i,s,5),this.setIndex(u),this.setAttribute("position",new Ye(h,3)),this.setAttribute("normal",new Ye(f,3)),this.setAttribute("uv",new Ye(p,2));function y(M,x,_,w,E,T,U,P,D,F,C){const b=T/D,N=U/F,q=T/2,Y=U/2,K=P/2,le=D+1,$=F+1;let pe=0,J=0;const xe=new L;for(let me=0;me<$;me++){const Se=me*N-Y;for(let Qe=0;Qe<le;Qe++){const Je=Qe*b-q;xe[M]=Je*w,xe[x]=Se*E,xe[_]=K,h.push(xe.x,xe.y,xe.z),xe[M]=0,xe[x]=0,xe[_]=P>0?1:-1,f.push(xe.x,xe.y,xe.z),p.push(Qe/D),p.push(1-me/F),pe+=1}}for(let me=0;me<F;me++)for(let Se=0;Se<D;Se++){const Qe=m+Se+le*me,Je=m+Se+le*(me+1),se=m+(Se+1)+le*(me+1),ge=m+(Se+1)+le*me;u.push(Qe,Je,ge),u.push(Je,se,ge),J+=6}c.addGroup(g,J,C),g+=J,m+=pe}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Fs(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Do(r){const e={};for(const t in r){e[t]={};for(const n in r[t]){const i=r[t][n];i&&(i.isColor||i.isMatrix3||i.isMatrix4||i.isVector2||i.isVector3||i.isVector4||i.isTexture||i.isQuaternion)?i.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][n]=null):e[t][n]=i.clone():Array.isArray(i)?e[t][n]=i.slice():e[t][n]=i}}return e}function kn(r){const e={};for(let t=0;t<r.length;t++){const n=Do(r[t]);for(const i in n)e[i]=n[i]}return e}function aM(r){const e=[];for(let t=0;t<r.length;t++)e.push(r[t].clone());return e}function w_(r){const e=r.getRenderTarget();return e===null?r.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Pt.workingColorSpace}const Xu={clone:Do,merge:kn};var lM=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,cM=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class _i extends Nn{static get type(){return"ShaderMaterial"}constructor(e){super(),this.isShaderMaterial=!0,this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=lM,this.fragmentShader=cM,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Do(e.uniforms),this.uniformsGroups=aM(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const i in this.uniforms){const l=this.uniforms[i].value;l&&l.isTexture?t.uniforms[i]={type:"t",value:l.toJSON(e).uuid}:l&&l.isColor?t.uniforms[i]={type:"c",value:l.getHex()}:l&&l.isVector2?t.uniforms[i]={type:"v2",value:l.toArray()}:l&&l.isVector3?t.uniforms[i]={type:"v3",value:l.toArray()}:l&&l.isVector4?t.uniforms[i]={type:"v4",value:l.toArray()}:l&&l.isMatrix3?t.uniforms[i]={type:"m3",value:l.toArray()}:l&&l.isMatrix4?t.uniforms[i]={type:"m4",value:l.toArray()}:t.uniforms[i]={value:l}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const n={};for(const i in this.extensions)this.extensions[i]===!0&&(n[i]=!0);return Object.keys(n).length>0&&(t.extensions=n),t}}class el extends Dt{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new ut,this.projectionMatrix=new ut,this.projectionMatrixInverse=new ut,this.coordinateSystem=Yi}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Fr=new L,Yg=new ae,qg=new ae;class tn extends el{constructor(e=50,t=1,n=.1,i=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=n,this.far=i,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=Lo*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(bs*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return Lo*2*Math.atan(Math.tan(bs*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,n){Fr.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Fr.x,Fr.y).multiplyScalar(-e/Fr.z),Fr.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),n.set(Fr.x,Fr.y).multiplyScalar(-e/Fr.z)}getViewSize(e,t){return this.getViewBounds(e,Yg,qg),t.subVectors(qg,Yg)}setViewOffset(e,t,n,i,s,l){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=n,this.view.offsetY=i,this.view.width=s,this.view.height=l,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(bs*.5*this.fov)/this.zoom,n=2*t,i=this.aspect*n,s=-.5*i;const l=this.view;if(this.view!==null&&this.view.enabled){const u=l.fullWidth,h=l.fullHeight;s+=l.offsetX*i/u,t-=l.offsetY*n/h,i*=l.width/u,n*=l.height/h}const c=this.filmOffset;c!==0&&(s+=e*c/this.getFilmWidth()),this.projectionMatrix.makePerspective(s,s+i,t,t-n,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const ho=-90,fo=1;class T_ extends Dt{constructor(e,t,n){super(),this.type="CubeCamera",this.renderTarget=n,this.coordinateSystem=null,this.activeMipmapLevel=0;const i=new tn(ho,fo,e,t);i.layers=this.layers,this.add(i);const s=new tn(ho,fo,e,t);s.layers=this.layers,this.add(s);const l=new tn(ho,fo,e,t);l.layers=this.layers,this.add(l);const c=new tn(ho,fo,e,t);c.layers=this.layers,this.add(c);const u=new tn(ho,fo,e,t);u.layers=this.layers,this.add(u);const h=new tn(ho,fo,e,t);h.layers=this.layers,this.add(h)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[n,i,s,l,c,u]=t;for(const h of t)this.remove(h);if(e===Yi)n.up.set(0,1,0),n.lookAt(1,0,0),i.up.set(0,1,0),i.lookAt(-1,0,0),s.up.set(0,0,-1),s.lookAt(0,1,0),l.up.set(0,0,1),l.lookAt(0,-1,0),c.up.set(0,1,0),c.lookAt(0,0,1),u.up.set(0,1,0),u.lookAt(0,0,-1);else if(e===ka)n.up.set(0,-1,0),n.lookAt(-1,0,0),i.up.set(0,-1,0),i.lookAt(1,0,0),s.up.set(0,0,1),s.lookAt(0,1,0),l.up.set(0,0,-1),l.lookAt(0,-1,0),c.up.set(0,-1,0),c.lookAt(0,0,1),u.up.set(0,-1,0),u.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const h of t)this.add(h),h.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:n,activeMipmapLevel:i}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[s,l,c,u,h,f]=this.children,p=e.getRenderTarget(),m=e.getActiveCubeFace(),g=e.getActiveMipmapLevel(),y=e.xr.enabled;e.xr.enabled=!1;const M=n.texture.generateMipmaps;n.texture.generateMipmaps=!1,e.setRenderTarget(n,0,i),e.render(t,s),e.setRenderTarget(n,1,i),e.render(t,l),e.setRenderTarget(n,2,i),e.render(t,c),e.setRenderTarget(n,3,i),e.render(t,u),e.setRenderTarget(n,4,i),e.render(t,h),n.texture.generateMipmaps=M,e.setRenderTarget(n,5,i),e.render(t,f),e.setRenderTarget(p,m,g),e.xr.enabled=y,n.texture.needsPMREMUpdate=!0}}class tl extends Kt{constructor(e,t,n,i,s,l,c,u,h,f){e=e!==void 0?e:[],t=t!==void 0?t:_r,super(e,t,n,i,s,l,c,u,h,f),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class A_ extends Ci{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const n={width:e,height:e,depth:1},i=[n,n,n,n,n,n];this.texture=new tl(i,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:cn}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const n={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},i=new Fs(5,5,5),s=new _i({name:"CubemapFromEquirect",uniforms:Do(n.uniforms),vertexShader:n.vertexShader,fragmentShader:n.fragmentShader,side:Vn,blending:mr});s.uniforms.tEquirect.value=t;const l=new nn(i,s),c=t.minFilter;return t.minFilter===Xi&&(t.minFilter=cn),new T_(1,10,this).update(e,l),t.minFilter=c,l.geometry.dispose(),l.material.dispose(),this}clear(e,t,n,i){const s=e.getRenderTarget();for(let l=0;l<6;l++)e.setRenderTarget(this,l),e.clear(t,n,i);e.setRenderTarget(s)}}const ed=new L,uM=new L,hM=new gt;class hr{constructor(e=new L(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,n,i){return this.normal.set(e,t,n),this.constant=i,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,n){const i=ed.subVectors(n,t).cross(uM.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(i,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const n=e.delta(ed),i=this.normal.dot(n);if(i===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const s=-(e.start.dot(this.normal)+this.constant)/i;return s<0||s>1?null:t.copy(e.start).addScaledVector(n,s)}intersectsLine(e){const t=this.distanceToPoint(e.start),n=this.distanceToPoint(e.end);return t<0&&n>0||n<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const n=t||hM.getNormalMatrix(e),i=this.coplanarPoint(ed).applyMatrix4(e),s=this.normal.applyMatrix3(n).normalize();return this.constant=-i.dot(s),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const os=new yn,Tc=new L;class nl{constructor(e=new hr,t=new hr,n=new hr,i=new hr,s=new hr,l=new hr){this.planes=[e,t,n,i,s,l]}set(e,t,n,i,s,l){const c=this.planes;return c[0].copy(e),c[1].copy(t),c[2].copy(n),c[3].copy(i),c[4].copy(s),c[5].copy(l),this}copy(e){const t=this.planes;for(let n=0;n<6;n++)t[n].copy(e.planes[n]);return this}setFromProjectionMatrix(e,t=Yi){const n=this.planes,i=e.elements,s=i[0],l=i[1],c=i[2],u=i[3],h=i[4],f=i[5],p=i[6],m=i[7],g=i[8],y=i[9],M=i[10],x=i[11],_=i[12],w=i[13],E=i[14],T=i[15];if(n[0].setComponents(u-s,m-h,x-g,T-_).normalize(),n[1].setComponents(u+s,m+h,x+g,T+_).normalize(),n[2].setComponents(u+l,m+f,x+y,T+w).normalize(),n[3].setComponents(u-l,m-f,x-y,T-w).normalize(),n[4].setComponents(u-c,m-p,x-M,T-E).normalize(),t===Yi)n[5].setComponents(u+c,m+p,x+M,T+E).normalize();else if(t===ka)n[5].setComponents(c,p,M,E).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),os.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),os.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(os)}intersectsSprite(e){return os.center.set(0,0,0),os.radius=.7071067811865476,os.applyMatrix4(e.matrixWorld),this.intersectsSphere(os)}intersectsSphere(e){const t=this.planes,n=e.center,i=-e.radius;for(let s=0;s<6;s++)if(t[s].distanceToPoint(n)<i)return!1;return!0}intersectsBox(e){const t=this.planes;for(let n=0;n<6;n++){const i=t[n];if(Tc.x=i.normal.x>0?e.max.x:e.min.x,Tc.y=i.normal.y>0?e.max.y:e.min.y,Tc.z=i.normal.z>0?e.max.z:e.min.z,i.distanceToPoint(Tc)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let n=0;n<6;n++)if(t[n].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}function b_(){let r=null,e=!1,t=null,n=null;function i(s,l){t(s,l),n=r.requestAnimationFrame(i)}return{start:function(){e!==!0&&t!==null&&(n=r.requestAnimationFrame(i),e=!0)},stop:function(){r.cancelAnimationFrame(n),e=!1},setAnimationLoop:function(s){t=s},setContext:function(s){r=s}}}function fM(r){const e=new WeakMap;function t(c,u){const h=c.array,f=c.usage,p=h.byteLength,m=r.createBuffer();r.bindBuffer(u,m),r.bufferData(u,h,f),c.onUploadCallback();let g;if(h instanceof Float32Array)g=r.FLOAT;else if(h instanceof Uint16Array)c.isFloat16BufferAttribute?g=r.HALF_FLOAT:g=r.UNSIGNED_SHORT;else if(h instanceof Int16Array)g=r.SHORT;else if(h instanceof Uint32Array)g=r.UNSIGNED_INT;else if(h instanceof Int32Array)g=r.INT;else if(h instanceof Int8Array)g=r.BYTE;else if(h instanceof Uint8Array)g=r.UNSIGNED_BYTE;else if(h instanceof Uint8ClampedArray)g=r.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+h);return{buffer:m,type:g,bytesPerElement:h.BYTES_PER_ELEMENT,version:c.version,size:p}}function n(c,u,h){const f=u.array,p=u.updateRanges;if(r.bindBuffer(h,c),p.length===0)r.bufferSubData(h,0,f);else{p.sort((g,y)=>g.start-y.start);let m=0;for(let g=1;g<p.length;g++){const y=p[m],M=p[g];M.start<=y.start+y.count+1?y.count=Math.max(y.count,M.start+M.count-y.start):(++m,p[m]=M)}p.length=m+1;for(let g=0,y=p.length;g<y;g++){const M=p[g];r.bufferSubData(h,M.start*f.BYTES_PER_ELEMENT,f,M.start,M.count)}u.clearUpdateRanges()}u.onUploadCallback()}function i(c){return c.isInterleavedBufferAttribute&&(c=c.data),e.get(c)}function s(c){c.isInterleavedBufferAttribute&&(c=c.data);const u=e.get(c);u&&(r.deleteBuffer(u.buffer),e.delete(c))}function l(c,u){if(c.isInterleavedBufferAttribute&&(c=c.data),c.isGLBufferAttribute){const f=e.get(c);(!f||f.version<c.version)&&e.set(c,{buffer:c.buffer,type:c.type,bytesPerElement:c.elementSize,version:c.version});return}const h=e.get(c);if(h===void 0)e.set(c,t(c,u));else if(h.version<c.version){if(h.size!==c.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");n(h.buffer,c,u),h.version=c.version}}return{get:i,remove:s,update:l}}class Bo extends xt{constructor(e=1,t=1,n=1,i=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:n,heightSegments:i};const s=e/2,l=t/2,c=Math.floor(n),u=Math.floor(i),h=c+1,f=u+1,p=e/c,m=t/u,g=[],y=[],M=[],x=[];for(let _=0;_<f;_++){const w=_*m-l;for(let E=0;E<h;E++){const T=E*p-s;y.push(T,-w,0),M.push(0,0,1),x.push(E/c),x.push(1-_/u)}}for(let _=0;_<u;_++)for(let w=0;w<c;w++){const E=w+h*_,T=w+h*(_+1),U=w+1+h*(_+1),P=w+1+h*_;g.push(E,T,P),g.push(T,U,P)}this.setIndex(g),this.setAttribute("position",new Ye(y,3)),this.setAttribute("normal",new Ye(M,3)),this.setAttribute("uv",new Ye(x,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Bo(e.width,e.height,e.widthSegments,e.heightSegments)}}var dM=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,pM=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,mM=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,gM=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,vM=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,_M=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,yM=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,xM=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,SM=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec3 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 ).rgb;
	}
#endif`,MM=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,EM=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,wM=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,TM=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,AM=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,bM=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,CM=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,RM=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,PM=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,IM=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,LM=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,DM=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,UM=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,NM=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif
#ifdef USE_BATCHING_COLOR
	vec3 batchingColor = getBatchingColor( getIndirectIndex( gl_DrawID ) );
	vColor.xyz *= batchingColor.xyz;
#endif`,OM=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
mat3 transposeMat3( const in mat3 m ) {
	mat3 tmp;
	tmp[ 0 ] = vec3( m[ 0 ].x, m[ 1 ].x, m[ 2 ].x );
	tmp[ 1 ] = vec3( m[ 0 ].y, m[ 1 ].y, m[ 2 ].y );
	tmp[ 2 ] = vec3( m[ 0 ].z, m[ 1 ].z, m[ 2 ].z );
	return tmp;
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,FM=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,BM=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,zM=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,kM=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,HM=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,VM=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,GM="gl_FragColor = linearToOutputTexel( gl_FragColor );",WM=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,XM=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
	#else
		vec4 envColor = vec4( 0.0 );
	#endif
	#ifdef ENVMAP_BLENDING_MULTIPLY
		outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_MIX )
		outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_ADD )
		outgoingLight += envColor.xyz * specularStrength * reflectivity;
	#endif
#endif`,YM=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,qM=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,ZM=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,jM=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,JM=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,KM=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,QM=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,$M=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,eE=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,tE=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,nE=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,iE=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,rE=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif`,sE=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, roughness * roughness) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,oE=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,aE=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,lE=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,cE=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,uE=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb * ( 1.0 - metalnessFactor );
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = mix( min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = mix( vec3( 0.04 ), diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.07, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,hE=`struct PhysicalMaterial {
	vec3 diffuseColor;
	float roughness;
	vec3 specularColor;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		float v = 0.5 / ( gv + gl );
		return saturate(v);
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColor;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transposeMat3( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float a = roughness < 0.25 ? -339.2 * r2 + 161.4 * roughness - 25.9 : -8.48 * r2 + 14.3 * roughness - 9.95;
	float b = roughness < 0.25 ? 44.0 * r2 - 23.7 * roughness + 3.26 : 1.97 * r2 - 3.27 * roughness + 0.72;
	float DG = exp( a * dotNV + b ) + ( roughness < 0.25 ? 0.0 : 0.1 * ( roughness - 0.25 ) );
	return saturate( DG * RECIPROCAL_PI );
}
vec2 DFGApprox( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	const vec4 c0 = vec4( - 1, - 0.0275, - 0.572, 0.022 );
	const vec4 c1 = vec4( 1, 0.0425, 1.04, - 0.04 );
	vec4 r = roughness * c0 + c1;
	float a004 = min( r.x * r.x, exp2( - 9.28 * dotNV ) ) * r.x + r.y;
	vec2 fab = vec2( - 1.04, 1.04 ) * a004 + r.zw;
	return fab;
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColor * t2.x + ( vec3( 1.0 ) - material.specularColor ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseColor * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
	#endif
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnel, material.roughness, singleScattering, multiScattering );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScattering, multiScattering );
	#endif
	vec3 totalScattering = singleScattering + multiScattering;
	vec3 diffuse = material.diffuseColor * ( 1.0 - max( max( totalScattering.r, totalScattering.g ), totalScattering.b ) );
	reflectedLight.indirectSpecular += radiance * singleScattering;
	reflectedLight.indirectSpecular += multiScattering * cosineWeightedIrradiance;
	reflectedLight.indirectDiffuse += diffuse * cosineWeightedIrradiance;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,fE=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnel = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,dE=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD ) && defined( ENVMAP_TYPE_CUBE_UV )
		iblIrradiance += getIBLIrradiance( geometryNormal );
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,pE=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,mE=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,gE=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,vE=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,_E=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,yE=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,xE=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,SE=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,ME=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,EE=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,wE=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,TE=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,AE=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,bE=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,CE=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,RE=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,PE=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,IE=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,LE=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,DE=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,UE=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,NE=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,OE=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,FE=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,BE=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,zE=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,kE=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,HE=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return depth * ( near - far ) - near;
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return ( near * far ) / ( ( far - near ) * depth - far );
}`,VE=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,GE=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,WE=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,XE=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,YE=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,qE=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,ZE=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform sampler2D pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {
		return step( compare, unpackRGBAToDepth( texture2D( depths, uv ) ) );
	}
	vec2 texture2DDistribution( sampler2D shadow, vec2 uv ) {
		return unpackRGBATo2Half( texture2D( shadow, uv ) );
	}
	float VSMShadow (sampler2D shadow, vec2 uv, float compare ){
		float occlusion = 1.0;
		vec2 distribution = texture2DDistribution( shadow, uv );
		float hard_shadow = step( compare , distribution.x );
		if (hard_shadow != 1.0 ) {
			float distance = compare - distribution.x ;
			float variance = max( 0.00000, distribution.y * distribution.y );
			float softness_probability = variance / (variance + distance * distance );			softness_probability = clamp( ( softness_probability - 0.3 ) / ( 0.95 - 0.3 ), 0.0, 1.0 );			occlusion = clamp( max( hard_shadow, softness_probability ), 0.0, 1.0 );
		}
		return occlusion;
	}
	float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
		float shadow = 1.0;
		shadowCoord.xyz /= shadowCoord.w;
		shadowCoord.z += shadowBias;
		bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
		bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
		if ( frustumTest ) {
		#if defined( SHADOWMAP_TYPE_PCF )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx0 = - texelSize.x * shadowRadius;
			float dy0 = - texelSize.y * shadowRadius;
			float dx1 = + texelSize.x * shadowRadius;
			float dy1 = + texelSize.y * shadowRadius;
			float dx2 = dx0 / 2.0;
			float dy2 = dy0 / 2.0;
			float dx3 = dx1 / 2.0;
			float dy3 = dy1 / 2.0;
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
			) * ( 1.0 / 17.0 );
		#elif defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx = texelSize.x;
			float dy = texelSize.y;
			vec2 uv = shadowCoord.xy;
			vec2 f = fract( uv * shadowMapSize + 0.5 );
			uv -= f * texelSize;
			shadow = (
				texture2DCompare( shadowMap, uv, shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( dx, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( 0.0, dy ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + texelSize, shadowCoord.z ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, 0.0 ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 0.0 ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, dy ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( 0.0, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 0.0, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( texture2DCompare( shadowMap, uv + vec2( dx, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( dx, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( mix( texture2DCompare( shadowMap, uv + vec2( -dx, -dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, -dy ), shadowCoord.z ),
						  f.x ),
					 mix( texture2DCompare( shadowMap, uv + vec2( -dx, 2.0 * dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 2.0 * dy ), shadowCoord.z ),
						  f.x ),
					 f.y )
			) * ( 1.0 / 9.0 );
		#elif defined( SHADOWMAP_TYPE_VSM )
			shadow = VSMShadow( shadowMap, shadowCoord.xy, shadowCoord.z );
		#else
			shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );
		#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	vec2 cubeToUV( vec3 v, float texelSizeY ) {
		vec3 absV = abs( v );
		float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
		absV *= scaleToCube;
		v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );
		vec2 planar = v.xy;
		float almostATexel = 1.5 * texelSizeY;
		float almostOne = 1.0 - almostATexel;
		if ( absV.z >= almostOne ) {
			if ( v.z > 0.0 )
				planar.x = 4.0 - v.x;
		} else if ( absV.x >= almostOne ) {
			float signX = sign( v.x );
			planar.x = v.z * signX + 2.0 * signX;
		} else if ( absV.y >= almostOne ) {
			float signY = sign( v.y );
			planar.x = v.x + 2.0 * signY + 2.0;
			planar.y = v.z * signY - 2.0;
		}
		return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );
	}
	float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		
		float lightToPositionLength = length( lightToPosition );
		if ( lightToPositionLength - shadowCameraFar <= 0.0 && lightToPositionLength - shadowCameraNear >= 0.0 ) {
			float dp = ( lightToPositionLength - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear );			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );
			#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT ) || defined( SHADOWMAP_TYPE_VSM )
				vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;
				shadow = (
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
				) * ( 1.0 / 9.0 );
			#else
				shadow = texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );
			#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
#endif`,jE=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,JE=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,KE=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,QE=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,$E=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,ew=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,tw=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,nw=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,iw=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,rw=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,sw=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,ow=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseColor, material.specularColor, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,aw=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
		
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
		
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		
		#else
		
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,lw=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,cw=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,uw=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,hw=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const fw=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,dw=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,pw=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,mw=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,gw=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,vw=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,_w=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,yw=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	float fragCoordZ = 0.5 * vHighPrecisionZW[0] / vHighPrecisionZW[1] + 0.5;
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,xw=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,Sw=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = packDepthToRGBA( dist );
}`,Mw=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,Ew=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,ww=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Tw=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Aw=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,bw=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Cw=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Rw=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Pw=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,Iw=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Lw=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,Dw=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <packing>
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( packNormalToRGB( normal ), diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,Uw=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Nw=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Ow=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,Fw=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
		float sheenEnergyComp = 1.0 - 0.157 * max3( material.sheenColor );
		outgoingLight = outgoingLight * sheenEnergyComp + sheenSpecularDirect + sheenSpecularIndirect;
	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Bw=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,zw=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,kw=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,Hw=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Vw=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Gw=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <packing>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,Ww=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Xw=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,yt={alphahash_fragment:dM,alphahash_pars_fragment:pM,alphamap_fragment:mM,alphamap_pars_fragment:gM,alphatest_fragment:vM,alphatest_pars_fragment:_M,aomap_fragment:yM,aomap_pars_fragment:xM,batching_pars_vertex:SM,batching_vertex:MM,begin_vertex:EM,beginnormal_vertex:wM,bsdfs:TM,iridescence_fragment:AM,bumpmap_pars_fragment:bM,clipping_planes_fragment:CM,clipping_planes_pars_fragment:RM,clipping_planes_pars_vertex:PM,clipping_planes_vertex:IM,color_fragment:LM,color_pars_fragment:DM,color_pars_vertex:UM,color_vertex:NM,common:OM,cube_uv_reflection_fragment:FM,defaultnormal_vertex:BM,displacementmap_pars_vertex:zM,displacementmap_vertex:kM,emissivemap_fragment:HM,emissivemap_pars_fragment:VM,colorspace_fragment:GM,colorspace_pars_fragment:WM,envmap_fragment:XM,envmap_common_pars_fragment:YM,envmap_pars_fragment:qM,envmap_pars_vertex:ZM,envmap_physical_pars_fragment:sE,envmap_vertex:jM,fog_vertex:JM,fog_pars_vertex:KM,fog_fragment:QM,fog_pars_fragment:$M,gradientmap_pars_fragment:eE,lightmap_pars_fragment:tE,lights_lambert_fragment:nE,lights_lambert_pars_fragment:iE,lights_pars_begin:rE,lights_toon_fragment:oE,lights_toon_pars_fragment:aE,lights_phong_fragment:lE,lights_phong_pars_fragment:cE,lights_physical_fragment:uE,lights_physical_pars_fragment:hE,lights_fragment_begin:fE,lights_fragment_maps:dE,lights_fragment_end:pE,logdepthbuf_fragment:mE,logdepthbuf_pars_fragment:gE,logdepthbuf_pars_vertex:vE,logdepthbuf_vertex:_E,map_fragment:yE,map_pars_fragment:xE,map_particle_fragment:SE,map_particle_pars_fragment:ME,metalnessmap_fragment:EE,metalnessmap_pars_fragment:wE,morphinstance_vertex:TE,morphcolor_vertex:AE,morphnormal_vertex:bE,morphtarget_pars_vertex:CE,morphtarget_vertex:RE,normal_fragment_begin:PE,normal_fragment_maps:IE,normal_pars_fragment:LE,normal_pars_vertex:DE,normal_vertex:UE,normalmap_pars_fragment:NE,clearcoat_normal_fragment_begin:OE,clearcoat_normal_fragment_maps:FE,clearcoat_pars_fragment:BE,iridescence_pars_fragment:zE,opaque_fragment:kE,packing:HE,premultiplied_alpha_fragment:VE,project_vertex:GE,dithering_fragment:WE,dithering_pars_fragment:XE,roughnessmap_fragment:YE,roughnessmap_pars_fragment:qE,shadowmap_pars_fragment:ZE,shadowmap_pars_vertex:jE,shadowmap_vertex:JE,shadowmask_pars_fragment:KE,skinbase_vertex:QE,skinning_pars_vertex:$E,skinning_vertex:ew,skinnormal_vertex:tw,specularmap_fragment:nw,specularmap_pars_fragment:iw,tonemapping_fragment:rw,tonemapping_pars_fragment:sw,transmission_fragment:ow,transmission_pars_fragment:aw,uv_pars_fragment:lw,uv_pars_vertex:cw,uv_vertex:uw,worldpos_vertex:hw,background_vert:fw,background_frag:dw,backgroundCube_vert:pw,backgroundCube_frag:mw,cube_vert:gw,cube_frag:vw,depth_vert:_w,depth_frag:yw,distanceRGBA_vert:xw,distanceRGBA_frag:Sw,equirect_vert:Mw,equirect_frag:Ew,linedashed_vert:ww,linedashed_frag:Tw,meshbasic_vert:Aw,meshbasic_frag:bw,meshlambert_vert:Cw,meshlambert_frag:Rw,meshmatcap_vert:Pw,meshmatcap_frag:Iw,meshnormal_vert:Lw,meshnormal_frag:Dw,meshphong_vert:Uw,meshphong_frag:Nw,meshphysical_vert:Ow,meshphysical_frag:Fw,meshtoon_vert:Bw,meshtoon_frag:zw,points_vert:kw,points_frag:Hw,shadow_vert:Vw,shadow_frag:Gw,sprite_vert:Ww,sprite_frag:Xw},be={common:{diffuse:{value:new Be(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new gt},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new gt}},envmap:{envMap:{value:null},envMapRotation:{value:new gt},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new gt}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new gt}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new gt},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new gt},normalScale:{value:new ae(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new gt},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new gt}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new gt}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new gt}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new Be(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new Be(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0},uvTransform:{value:new gt}},sprite:{diffuse:{value:new Be(16777215)},opacity:{value:1},center:{value:new ae(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new gt},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0}}},Ai={basic:{uniforms:kn([be.common,be.specularmap,be.envmap,be.aomap,be.lightmap,be.fog]),vertexShader:yt.meshbasic_vert,fragmentShader:yt.meshbasic_frag},lambert:{uniforms:kn([be.common,be.specularmap,be.envmap,be.aomap,be.lightmap,be.emissivemap,be.bumpmap,be.normalmap,be.displacementmap,be.fog,be.lights,{emissive:{value:new Be(0)}}]),vertexShader:yt.meshlambert_vert,fragmentShader:yt.meshlambert_frag},phong:{uniforms:kn([be.common,be.specularmap,be.envmap,be.aomap,be.lightmap,be.emissivemap,be.bumpmap,be.normalmap,be.displacementmap,be.fog,be.lights,{emissive:{value:new Be(0)},specular:{value:new Be(1118481)},shininess:{value:30}}]),vertexShader:yt.meshphong_vert,fragmentShader:yt.meshphong_frag},standard:{uniforms:kn([be.common,be.envmap,be.aomap,be.lightmap,be.emissivemap,be.bumpmap,be.normalmap,be.displacementmap,be.roughnessmap,be.metalnessmap,be.fog,be.lights,{emissive:{value:new Be(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:yt.meshphysical_vert,fragmentShader:yt.meshphysical_frag},toon:{uniforms:kn([be.common,be.aomap,be.lightmap,be.emissivemap,be.bumpmap,be.normalmap,be.displacementmap,be.gradientmap,be.fog,be.lights,{emissive:{value:new Be(0)}}]),vertexShader:yt.meshtoon_vert,fragmentShader:yt.meshtoon_frag},matcap:{uniforms:kn([be.common,be.bumpmap,be.normalmap,be.displacementmap,be.fog,{matcap:{value:null}}]),vertexShader:yt.meshmatcap_vert,fragmentShader:yt.meshmatcap_frag},points:{uniforms:kn([be.points,be.fog]),vertexShader:yt.points_vert,fragmentShader:yt.points_frag},dashed:{uniforms:kn([be.common,be.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:yt.linedashed_vert,fragmentShader:yt.linedashed_frag},depth:{uniforms:kn([be.common,be.displacementmap]),vertexShader:yt.depth_vert,fragmentShader:yt.depth_frag},normal:{uniforms:kn([be.common,be.bumpmap,be.normalmap,be.displacementmap,{opacity:{value:1}}]),vertexShader:yt.meshnormal_vert,fragmentShader:yt.meshnormal_frag},sprite:{uniforms:kn([be.sprite,be.fog]),vertexShader:yt.sprite_vert,fragmentShader:yt.sprite_frag},background:{uniforms:{uvTransform:{value:new gt},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:yt.background_vert,fragmentShader:yt.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new gt}},vertexShader:yt.backgroundCube_vert,fragmentShader:yt.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:yt.cube_vert,fragmentShader:yt.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:yt.equirect_vert,fragmentShader:yt.equirect_frag},distanceRGBA:{uniforms:kn([be.common,be.displacementmap,{referencePosition:{value:new L},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:yt.distanceRGBA_vert,fragmentShader:yt.distanceRGBA_frag},shadow:{uniforms:kn([be.lights,be.fog,{color:{value:new Be(0)},opacity:{value:1}}]),vertexShader:yt.shadow_vert,fragmentShader:yt.shadow_frag}};Ai.physical={uniforms:kn([Ai.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new gt},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new gt},clearcoatNormalScale:{value:new ae(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new gt},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new gt},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new gt},sheen:{value:0},sheenColor:{value:new Be(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new gt},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new gt},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new gt},transmissionSamplerSize:{value:new ae},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new gt},attenuationDistance:{value:0},attenuationColor:{value:new Be(0)},specularColor:{value:new Be(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new gt},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new gt},anisotropyVector:{value:new ae},anisotropyMap:{value:null},anisotropyMapTransform:{value:new gt}}]),vertexShader:yt.meshphysical_vert,fragmentShader:yt.meshphysical_frag};const Ac={r:0,b:0,g:0},as=new ai,Yw=new ut;function qw(r,e,t,n,i,s,l){const c=new Be(0);let u=s===!0?0:1,h,f,p=null,m=0,g=null;function y(w){let E=w.isScene===!0?w.background:null;return E&&E.isTexture&&(E=(w.backgroundBlurriness>0?t:e).get(E)),E}function M(w){let E=!1;const T=y(w);T===null?_(c,u):T&&T.isColor&&(_(T,1),E=!0);const U=r.xr.getEnvironmentBlendMode();U==="additive"?n.buffers.color.setClear(0,0,0,1,l):U==="alpha-blend"&&n.buffers.color.setClear(0,0,0,0,l),(r.autoClear||E)&&(n.buffers.depth.setTest(!0),n.buffers.depth.setMask(!0),n.buffers.color.setMask(!0),r.clear(r.autoClearColor,r.autoClearDepth,r.autoClearStencil))}function x(w,E){const T=y(E);T&&(T.isCubeTexture||T.mapping===Oo)?(f===void 0&&(f=new nn(new Fs(1,1,1),new _i({name:"BackgroundCubeMaterial",uniforms:Do(Ai.backgroundCube.uniforms),vertexShader:Ai.backgroundCube.vertexShader,fragmentShader:Ai.backgroundCube.fragmentShader,side:Vn,depthTest:!1,depthWrite:!1,fog:!1})),f.geometry.deleteAttribute("normal"),f.geometry.deleteAttribute("uv"),f.onBeforeRender=function(U,P,D){this.matrixWorld.copyPosition(D.matrixWorld)},Object.defineProperty(f.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),i.update(f)),as.copy(E.backgroundRotation),as.x*=-1,as.y*=-1,as.z*=-1,T.isCubeTexture&&T.isRenderTargetTexture===!1&&(as.y*=-1,as.z*=-1),f.material.uniforms.envMap.value=T,f.material.uniforms.flipEnvMap.value=T.isCubeTexture&&T.isRenderTargetTexture===!1?-1:1,f.material.uniforms.backgroundBlurriness.value=E.backgroundBlurriness,f.material.uniforms.backgroundIntensity.value=E.backgroundIntensity,f.material.uniforms.backgroundRotation.value.setFromMatrix4(Yw.makeRotationFromEuler(as)),f.material.toneMapped=Pt.getTransfer(T.colorSpace)!==Ft,(p!==T||m!==T.version||g!==r.toneMapping)&&(f.material.needsUpdate=!0,p=T,m=T.version,g=r.toneMapping),f.layers.enableAll(),w.unshift(f,f.geometry,f.material,0,0,null)):T&&T.isTexture&&(h===void 0&&(h=new nn(new Bo(2,2),new _i({name:"BackgroundMaterial",uniforms:Do(Ai.background.uniforms),vertexShader:Ai.background.vertexShader,fragmentShader:Ai.background.fragmentShader,side:vr,depthTest:!1,depthWrite:!1,fog:!1})),h.geometry.deleteAttribute("normal"),Object.defineProperty(h.material,"map",{get:function(){return this.uniforms.t2D.value}}),i.update(h)),h.material.uniforms.t2D.value=T,h.material.uniforms.backgroundIntensity.value=E.backgroundIntensity,h.material.toneMapped=Pt.getTransfer(T.colorSpace)!==Ft,T.matrixAutoUpdate===!0&&T.updateMatrix(),h.material.uniforms.uvTransform.value.copy(T.matrix),(p!==T||m!==T.version||g!==r.toneMapping)&&(h.material.needsUpdate=!0,p=T,m=T.version,g=r.toneMapping),h.layers.enableAll(),w.unshift(h,h.geometry,h.material,0,0,null))}function _(w,E){w.getRGB(Ac,w_(r)),n.buffers.color.setClear(Ac.r,Ac.g,Ac.b,E,l)}return{getClearColor:function(){return c},setClearColor:function(w,E=1){c.set(w),u=E,_(c,u)},getClearAlpha:function(){return u},setClearAlpha:function(w){u=w,_(c,u)},render:M,addToRenderList:x}}function Zw(r,e){const t=r.getParameter(r.MAX_VERTEX_ATTRIBS),n={},i=m(null);let s=i,l=!1;function c(b,N,q,Y,K){let le=!1;const $=p(Y,q,N);s!==$&&(s=$,h(s.object)),le=g(b,Y,q,K),le&&y(b,Y,q,K),K!==null&&e.update(K,r.ELEMENT_ARRAY_BUFFER),(le||l)&&(l=!1,T(b,N,q,Y),K!==null&&r.bindBuffer(r.ELEMENT_ARRAY_BUFFER,e.get(K).buffer))}function u(){return r.createVertexArray()}function h(b){return r.bindVertexArray(b)}function f(b){return r.deleteVertexArray(b)}function p(b,N,q){const Y=q.wireframe===!0;let K=n[b.id];K===void 0&&(K={},n[b.id]=K);let le=K[N.id];le===void 0&&(le={},K[N.id]=le);let $=le[Y];return $===void 0&&($=m(u()),le[Y]=$),$}function m(b){const N=[],q=[],Y=[];for(let K=0;K<t;K++)N[K]=0,q[K]=0,Y[K]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:N,enabledAttributes:q,attributeDivisors:Y,object:b,attributes:{},index:null}}function g(b,N,q,Y){const K=s.attributes,le=N.attributes;let $=0;const pe=q.getAttributes();for(const J in pe)if(pe[J].location>=0){const me=K[J];let Se=le[J];if(Se===void 0&&(J==="instanceMatrix"&&b.instanceMatrix&&(Se=b.instanceMatrix),J==="instanceColor"&&b.instanceColor&&(Se=b.instanceColor)),me===void 0||me.attribute!==Se||Se&&me.data!==Se.data)return!0;$++}return s.attributesNum!==$||s.index!==Y}function y(b,N,q,Y){const K={},le=N.attributes;let $=0;const pe=q.getAttributes();for(const J in pe)if(pe[J].location>=0){let me=le[J];me===void 0&&(J==="instanceMatrix"&&b.instanceMatrix&&(me=b.instanceMatrix),J==="instanceColor"&&b.instanceColor&&(me=b.instanceColor));const Se={};Se.attribute=me,me&&me.data&&(Se.data=me.data),K[J]=Se,$++}s.attributes=K,s.attributesNum=$,s.index=Y}function M(){const b=s.newAttributes;for(let N=0,q=b.length;N<q;N++)b[N]=0}function x(b){_(b,0)}function _(b,N){const q=s.newAttributes,Y=s.enabledAttributes,K=s.attributeDivisors;q[b]=1,Y[b]===0&&(r.enableVertexAttribArray(b),Y[b]=1),K[b]!==N&&(r.vertexAttribDivisor(b,N),K[b]=N)}function w(){const b=s.newAttributes,N=s.enabledAttributes;for(let q=0,Y=N.length;q<Y;q++)N[q]!==b[q]&&(r.disableVertexAttribArray(q),N[q]=0)}function E(b,N,q,Y,K,le,$){$===!0?r.vertexAttribIPointer(b,N,q,K,le):r.vertexAttribPointer(b,N,q,Y,K,le)}function T(b,N,q,Y){M();const K=Y.attributes,le=q.getAttributes(),$=N.defaultAttributeValues;for(const pe in le){const J=le[pe];if(J.location>=0){let xe=K[pe];if(xe===void 0&&(pe==="instanceMatrix"&&b.instanceMatrix&&(xe=b.instanceMatrix),pe==="instanceColor"&&b.instanceColor&&(xe=b.instanceColor)),xe!==void 0){const me=xe.normalized,Se=xe.itemSize,Qe=e.get(xe);if(Qe===void 0)continue;const Je=Qe.buffer,se=Qe.type,ge=Qe.bytesPerElement,Ve=se===r.INT||se===r.UNSIGNED_INT||xe.gpuType===$u;if(xe.isInterleavedBufferAttribute){const we=xe.data,et=we.stride,lt=xe.offset;if(we.isInstancedInterleavedBuffer){for(let tt=0;tt<J.locationSize;tt++)_(J.location+tt,we.meshPerAttribute);b.isInstancedMesh!==!0&&Y._maxInstanceCount===void 0&&(Y._maxInstanceCount=we.meshPerAttribute*we.count)}else for(let tt=0;tt<J.locationSize;tt++)x(J.location+tt);r.bindBuffer(r.ARRAY_BUFFER,Je);for(let tt=0;tt<J.locationSize;tt++)E(J.location+tt,Se/J.locationSize,se,me,et*ge,(lt+Se/J.locationSize*tt)*ge,Ve)}else{if(xe.isInstancedBufferAttribute){for(let we=0;we<J.locationSize;we++)_(J.location+we,xe.meshPerAttribute);b.isInstancedMesh!==!0&&Y._maxInstanceCount===void 0&&(Y._maxInstanceCount=xe.meshPerAttribute*xe.count)}else for(let we=0;we<J.locationSize;we++)x(J.location+we);r.bindBuffer(r.ARRAY_BUFFER,Je);for(let we=0;we<J.locationSize;we++)E(J.location+we,Se/J.locationSize,se,me,Se*ge,Se/J.locationSize*we*ge,Ve)}}else if($!==void 0){const me=$[pe];if(me!==void 0)switch(me.length){case 2:r.vertexAttrib2fv(J.location,me);break;case 3:r.vertexAttrib3fv(J.location,me);break;case 4:r.vertexAttrib4fv(J.location,me);break;default:r.vertexAttrib1fv(J.location,me)}}}}w()}function U(){F();for(const b in n){const N=n[b];for(const q in N){const Y=N[q];for(const K in Y)f(Y[K].object),delete Y[K];delete N[q]}delete n[b]}}function P(b){if(n[b.id]===void 0)return;const N=n[b.id];for(const q in N){const Y=N[q];for(const K in Y)f(Y[K].object),delete Y[K];delete N[q]}delete n[b.id]}function D(b){for(const N in n){const q=n[N];if(q[b.id]===void 0)continue;const Y=q[b.id];for(const K in Y)f(Y[K].object),delete Y[K];delete q[b.id]}}function F(){C(),l=!0,s!==i&&(s=i,h(s.object))}function C(){i.geometry=null,i.program=null,i.wireframe=!1}return{setup:c,reset:F,resetDefaultState:C,dispose:U,releaseStatesOfGeometry:P,releaseStatesOfProgram:D,initAttributes:M,enableAttribute:x,disableUnusedAttributes:w}}function jw(r,e,t){let n;function i(h){n=h}function s(h,f){r.drawArrays(n,h,f),t.update(f,n,1)}function l(h,f,p){p!==0&&(r.drawArraysInstanced(n,h,f,p),t.update(f,n,p))}function c(h,f,p){if(p===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(n,h,0,f,0,p);let g=0;for(let y=0;y<p;y++)g+=f[y];t.update(g,n,1)}function u(h,f,p,m){if(p===0)return;const g=e.get("WEBGL_multi_draw");if(g===null)for(let y=0;y<h.length;y++)l(h[y],f[y],m[y]);else{g.multiDrawArraysInstancedWEBGL(n,h,0,f,0,m,0,p);let y=0;for(let M=0;M<p;M++)y+=f[M]*m[M];t.update(y,n,1)}}this.setMode=i,this.render=s,this.renderInstances=l,this.renderMultiDraw=c,this.renderMultiDrawInstances=u}function Jw(r,e,t,n){let i;function s(){if(i!==void 0)return i;if(e.has("EXT_texture_filter_anisotropic")===!0){const D=e.get("EXT_texture_filter_anisotropic");i=r.getParameter(D.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else i=0;return i}function l(D){return!(D!==Dn&&n.convert(D)!==r.getParameter(r.IMPLEMENTATION_COLOR_READ_FORMAT))}function c(D){const F=D===Fo&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(D!==bi&&n.convert(D)!==r.getParameter(r.IMPLEMENTATION_COLOR_READ_TYPE)&&D!==Kn&&!F)}function u(D){if(D==="highp"){if(r.getShaderPrecisionFormat(r.VERTEX_SHADER,r.HIGH_FLOAT).precision>0&&r.getShaderPrecisionFormat(r.FRAGMENT_SHADER,r.HIGH_FLOAT).precision>0)return"highp";D="mediump"}return D==="mediump"&&r.getShaderPrecisionFormat(r.VERTEX_SHADER,r.MEDIUM_FLOAT).precision>0&&r.getShaderPrecisionFormat(r.FRAGMENT_SHADER,r.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let h=t.precision!==void 0?t.precision:"highp";const f=u(h);f!==h&&(console.warn("THREE.WebGLRenderer:",h,"not supported, using",f,"instead."),h=f);const p=t.logarithmicDepthBuffer===!0,m=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),g=r.getParameter(r.MAX_TEXTURE_IMAGE_UNITS),y=r.getParameter(r.MAX_VERTEX_TEXTURE_IMAGE_UNITS),M=r.getParameter(r.MAX_TEXTURE_SIZE),x=r.getParameter(r.MAX_CUBE_MAP_TEXTURE_SIZE),_=r.getParameter(r.MAX_VERTEX_ATTRIBS),w=r.getParameter(r.MAX_VERTEX_UNIFORM_VECTORS),E=r.getParameter(r.MAX_VARYING_VECTORS),T=r.getParameter(r.MAX_FRAGMENT_UNIFORM_VECTORS),U=y>0,P=r.getParameter(r.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:s,getMaxPrecision:u,textureFormatReadable:l,textureTypeReadable:c,precision:h,logarithmicDepthBuffer:p,reverseDepthBuffer:m,maxTextures:g,maxVertexTextures:y,maxTextureSize:M,maxCubemapSize:x,maxAttributes:_,maxVertexUniforms:w,maxVaryings:E,maxFragmentUniforms:T,vertexTextures:U,maxSamples:P}}function Kw(r){const e=this;let t=null,n=0,i=!1,s=!1;const l=new hr,c=new gt,u={value:null,needsUpdate:!1};this.uniform=u,this.numPlanes=0,this.numIntersection=0,this.init=function(p,m){const g=p.length!==0||m||n!==0||i;return i=m,n=p.length,g},this.beginShadows=function(){s=!0,f(null)},this.endShadows=function(){s=!1},this.setGlobalState=function(p,m){t=f(p,m,0)},this.setState=function(p,m,g){const y=p.clippingPlanes,M=p.clipIntersection,x=p.clipShadows,_=r.get(p);if(!i||y===null||y.length===0||s&&!x)s?f(null):h();else{const w=s?0:n,E=w*4;let T=_.clippingState||null;u.value=T,T=f(y,m,E,g);for(let U=0;U!==E;++U)T[U]=t[U];_.clippingState=T,this.numIntersection=M?this.numPlanes:0,this.numPlanes+=w}};function h(){u.value!==t&&(u.value=t,u.needsUpdate=n>0),e.numPlanes=n,e.numIntersection=0}function f(p,m,g,y){const M=p!==null?p.length:0;let x=null;if(M!==0){if(x=u.value,y!==!0||x===null){const _=g+M*4,w=m.matrixWorldInverse;c.getNormalMatrix(w),(x===null||x.length<_)&&(x=new Float32Array(_));for(let E=0,T=g;E!==M;++E,T+=4)l.copy(p[E]).applyMatrix4(w,c),l.normal.toArray(x,T),x[T+3]=l.constant}u.value=x,u.needsUpdate=!0}return e.numPlanes=M,e.numIntersection=0,x}}function Qw(r){let e=new WeakMap;function t(l,c){return c===Da?l.mapping=_r:c===Ua&&(l.mapping=Hr),l}function n(l){if(l&&l.isTexture){const c=l.mapping;if(c===Da||c===Ua)if(e.has(l)){const u=e.get(l).texture;return t(u,l.mapping)}else{const u=l.image;if(u&&u.height>0){const h=new A_(u.height);return h.fromEquirectangularTexture(r,l),e.set(l,h),l.addEventListener("dispose",i),t(h.texture,l.mapping)}else return null}}return l}function i(l){const c=l.target;c.removeEventListener("dispose",i);const u=e.get(c);u!==void 0&&(e.delete(c),u.dispose())}function s(){e=new WeakMap}return{get:n,dispose:s}}class kr extends el{constructor(e=-1,t=1,n=1,i=-1,s=.1,l=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=n,this.bottom=i,this.near=s,this.far=l,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,n,i,s,l){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=n,this.view.offsetY=i,this.view.width=s,this.view.height=l,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),n=(this.right+this.left)/2,i=(this.top+this.bottom)/2;let s=n-e,l=n+e,c=i+t,u=i-t;if(this.view!==null&&this.view.enabled){const h=(this.right-this.left)/this.view.fullWidth/this.zoom,f=(this.top-this.bottom)/this.view.fullHeight/this.zoom;s+=h*this.view.offsetX,l=s+h*this.view.width,c-=f*this.view.offsetY,u=c-f*this.view.height}this.projectionMatrix.makeOrthographic(s,l,c,u,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}const Ao=4,Zg=[.125,.215,.35,.446,.526,.582],xs=20,td=new kr,jg=new Be;let nd=null,id=0,rd=0,sd=!1;const ys=(1+Math.sqrt(5))/2,po=1/ys,Jg=[new L(-ys,po,0),new L(ys,po,0),new L(-po,0,ys),new L(po,0,ys),new L(0,ys,-po),new L(0,ys,po),new L(-1,1,-1),new L(1,1,-1),new L(-1,1,1),new L(1,1,1)];class Gd{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,n=.1,i=100){nd=this._renderer.getRenderTarget(),id=this._renderer.getActiveCubeFace(),rd=this._renderer.getActiveMipmapLevel(),sd=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(256);const s=this._allocateTargets();return s.depthBuffer=!0,this._sceneToCubeUV(e,n,i,s),t>0&&this._blur(s,0,0,t),this._applyPMREM(s),this._cleanup(s),s}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=$g(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Qg(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(nd,id,rd),this._renderer.xr.enabled=sd,e.scissorTest=!1,bc(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===_r||e.mapping===Hr?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),nd=this._renderer.getRenderTarget(),id=this._renderer.getActiveCubeFace(),rd=this._renderer.getActiveMipmapLevel(),sd=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const n=t||this._allocateTargets();return this._textureToCubeUV(e,n),this._applyPMREM(n),this._cleanup(n),n}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,n={magFilter:cn,minFilter:cn,generateMipmaps:!1,type:Fo,format:Dn,colorSpace:Ns,depthBuffer:!1},i=Kg(e,t,n);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=Kg(e,t,n);const{_lodMax:s}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=$w(s)),this._blurMaterial=e1(s,e,t)}return i}_compileMaterial(e){const t=new nn(this._lodPlanes[0],e);this._renderer.compile(t,td)}_sceneToCubeUV(e,t,n,i){const c=new tn(90,1,t,n),u=[1,-1,1,1,1,1],h=[1,1,1,-1,-1,-1],f=this._renderer,p=f.autoClear,m=f.toneMapping;f.getClearColor(jg),f.toneMapping=qi,f.autoClear=!1;const g=new Wr({name:"PMREM.Background",side:Vn,depthWrite:!1,depthTest:!1}),y=new nn(new Fs,g);let M=!1;const x=e.background;x?x.isColor&&(g.color.copy(x),e.background=null,M=!0):(g.color.copy(jg),M=!0);for(let _=0;_<6;_++){const w=_%3;w===0?(c.up.set(0,u[_],0),c.lookAt(h[_],0,0)):w===1?(c.up.set(0,0,u[_]),c.lookAt(0,h[_],0)):(c.up.set(0,u[_],0),c.lookAt(0,0,h[_]));const E=this._cubeSize;bc(i,w*E,_>2?E:0,E,E),f.setRenderTarget(i),M&&f.render(y,c),f.render(e,c)}y.geometry.dispose(),y.material.dispose(),f.toneMapping=m,f.autoClear=p,e.background=x}_textureToCubeUV(e,t){const n=this._renderer,i=e.mapping===_r||e.mapping===Hr;i?(this._cubemapMaterial===null&&(this._cubemapMaterial=$g()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Qg());const s=i?this._cubemapMaterial:this._equirectMaterial,l=new nn(this._lodPlanes[0],s),c=s.uniforms;c.envMap.value=e;const u=this._cubeSize;bc(t,0,0,3*u,2*u),n.setRenderTarget(t),n.render(l,td)}_applyPMREM(e){const t=this._renderer,n=t.autoClear;t.autoClear=!1;const i=this._lodPlanes.length;for(let s=1;s<i;s++){const l=Math.sqrt(this._sigmas[s]*this._sigmas[s]-this._sigmas[s-1]*this._sigmas[s-1]),c=Jg[(i-s-1)%Jg.length];this._blur(e,s-1,s,l,c)}t.autoClear=n}_blur(e,t,n,i,s){const l=this._pingPongRenderTarget;this._halfBlur(e,l,t,n,i,"latitudinal",s),this._halfBlur(l,e,n,n,i,"longitudinal",s)}_halfBlur(e,t,n,i,s,l,c){const u=this._renderer,h=this._blurMaterial;l!=="latitudinal"&&l!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const f=3,p=new nn(this._lodPlanes[i],h),m=h.uniforms,g=this._sizeLods[n]-1,y=isFinite(s)?Math.PI/(2*g):2*Math.PI/(2*xs-1),M=s/y,x=isFinite(s)?1+Math.floor(f*M):xs;x>xs&&console.warn(`sigmaRadians, ${s}, is too large and will clip, as it requested ${x} samples when the maximum is set to ${xs}`);const _=[];let w=0;for(let D=0;D<xs;++D){const F=D/M,C=Math.exp(-F*F/2);_.push(C),D===0?w+=C:D<x&&(w+=2*C)}for(let D=0;D<_.length;D++)_[D]=_[D]/w;m.envMap.value=e.texture,m.samples.value=x,m.weights.value=_,m.latitudinal.value=l==="latitudinal",c&&(m.poleAxis.value=c);const{_lodMax:E}=this;m.dTheta.value=y,m.mipInt.value=E-n;const T=this._sizeLods[i],U=3*T*(i>E-Ao?i-E+Ao:0),P=4*(this._cubeSize-T);bc(t,U,P,3*T,2*T),u.setRenderTarget(t),u.render(p,td)}}function $w(r){const e=[],t=[],n=[];let i=r;const s=r-Ao+1+Zg.length;for(let l=0;l<s;l++){const c=Math.pow(2,i);t.push(c);let u=1/c;l>r-Ao?u=Zg[l-r+Ao-1]:l===0&&(u=0),n.push(u);const h=1/(c-2),f=-h,p=1+h,m=[f,f,p,f,p,p,f,f,p,p,f,p],g=6,y=6,M=3,x=2,_=1,w=new Float32Array(M*y*g),E=new Float32Array(x*y*g),T=new Float32Array(_*y*g);for(let P=0;P<g;P++){const D=P%3*2/3-1,F=P>2?0:-1,C=[D,F,0,D+2/3,F,0,D+2/3,F+1,0,D,F,0,D+2/3,F+1,0,D,F+1,0];w.set(C,M*y*P),E.set(m,x*y*P);const b=[P,P,P,P,P,P];T.set(b,_*y*P)}const U=new xt;U.setAttribute("position",new zt(w,M)),U.setAttribute("uv",new zt(E,x)),U.setAttribute("faceIndex",new zt(T,_)),e.push(U),i>Ao&&i--}return{lodPlanes:e,sizeLods:t,sigmas:n}}function Kg(r,e,t){const n=new Ci(r,e,t);return n.texture.mapping=Oo,n.texture.name="PMREM.cubeUv",n.scissorTest=!0,n}function bc(r,e,t,n,i){r.viewport.set(e,t,n,i),r.scissor.set(e,t,n,i)}function e1(r,e,t){const n=new Float32Array(xs),i=new L(0,1,0);return new _i({name:"SphericalGaussianBlur",defines:{n:xs,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${r}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:n},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:i}},vertexShader:_p(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform int samples;
			uniform float weights[ n ];
			uniform bool latitudinal;
			uniform float dTheta;
			uniform float mipInt;
			uniform vec3 poleAxis;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			vec3 getSample( float theta, vec3 axis ) {

				float cosTheta = cos( theta );
				// Rodrigues' axis-angle rotation
				vec3 sampleDirection = vOutputDirection * cosTheta
					+ cross( axis, vOutputDirection ) * sin( theta )
					+ axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );

				return bilinearCubeUV( envMap, sampleDirection, mipInt );

			}

			void main() {

				vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );

				if ( all( equal( axis, vec3( 0.0 ) ) ) ) {

					axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );

				}

				axis = normalize( axis );

				gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
				gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );

				for ( int i = 1; i < n; i++ ) {

					if ( i >= samples ) {

						break;

					}

					float theta = dTheta * float( i );
					gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
					gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );

				}

			}
		`,blending:mr,depthTest:!1,depthWrite:!1})}function Qg(){return new _i({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:_p(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:mr,depthTest:!1,depthWrite:!1})}function $g(){return new _i({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:_p(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:mr,depthTest:!1,depthWrite:!1})}function _p(){return`

		precision mediump float;
		precision mediump int;

		attribute float faceIndex;

		varying vec3 vOutputDirection;

		// RH coordinate system; PMREM face-indexing convention
		vec3 getDirection( vec2 uv, float face ) {

			uv = 2.0 * uv - 1.0;

			vec3 direction = vec3( uv, 1.0 );

			if ( face == 0.0 ) {

				direction = direction.zyx; // ( 1, v, u ) pos x

			} else if ( face == 1.0 ) {

				direction = direction.xzy;
				direction.xz *= -1.0; // ( -u, 1, -v ) pos y

			} else if ( face == 2.0 ) {

				direction.x *= -1.0; // ( -u, v, 1 ) pos z

			} else if ( face == 3.0 ) {

				direction = direction.zyx;
				direction.xz *= -1.0; // ( -1, v, -u ) neg x

			} else if ( face == 4.0 ) {

				direction = direction.xzy;
				direction.xy *= -1.0; // ( -u, -1, v ) neg y

			} else if ( face == 5.0 ) {

				direction.z *= -1.0; // ( u, v, -1 ) neg z

			}

			return direction;

		}

		void main() {

			vOutputDirection = getDirection( uv, faceIndex );
			gl_Position = vec4( position, 1.0 );

		}
	`}function t1(r){let e=new WeakMap,t=null;function n(c){if(c&&c.isTexture){const u=c.mapping,h=u===Da||u===Ua,f=u===_r||u===Hr;if(h||f){let p=e.get(c);const m=p!==void 0?p.texture.pmremVersion:0;if(c.isRenderTargetTexture&&c.pmremVersion!==m)return t===null&&(t=new Gd(r)),p=h?t.fromEquirectangular(c,p):t.fromCubemap(c,p),p.texture.pmremVersion=c.pmremVersion,e.set(c,p),p.texture;if(p!==void 0)return p.texture;{const g=c.image;return h&&g&&g.height>0||f&&g&&i(g)?(t===null&&(t=new Gd(r)),p=h?t.fromEquirectangular(c):t.fromCubemap(c),p.texture.pmremVersion=c.pmremVersion,e.set(c,p),c.addEventListener("dispose",s),p.texture):null}}}return c}function i(c){let u=0;const h=6;for(let f=0;f<h;f++)c[f]!==void 0&&u++;return u===h}function s(c){const u=c.target;u.removeEventListener("dispose",s);const h=e.get(u);h!==void 0&&(e.delete(u),h.dispose())}function l(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:n,dispose:l}}function n1(r){const e={};function t(n){if(e[n]!==void 0)return e[n];let i;switch(n){case"WEBGL_depth_texture":i=r.getExtension("WEBGL_depth_texture")||r.getExtension("MOZ_WEBGL_depth_texture")||r.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":i=r.getExtension("EXT_texture_filter_anisotropic")||r.getExtension("MOZ_EXT_texture_filter_anisotropic")||r.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":i=r.getExtension("WEBGL_compressed_texture_s3tc")||r.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||r.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":i=r.getExtension("WEBGL_compressed_texture_pvrtc")||r.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:i=r.getExtension(n)}return e[n]=i,i}return{has:function(n){return t(n)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(n){const i=t(n);return i===null&&xa("THREE.WebGLRenderer: "+n+" extension not supported."),i}}}function i1(r,e,t,n){const i={},s=new WeakMap;function l(p){const m=p.target;m.index!==null&&e.remove(m.index);for(const y in m.attributes)e.remove(m.attributes[y]);for(const y in m.morphAttributes){const M=m.morphAttributes[y];for(let x=0,_=M.length;x<_;x++)e.remove(M[x])}m.removeEventListener("dispose",l),delete i[m.id];const g=s.get(m);g&&(e.remove(g),s.delete(m)),n.releaseStatesOfGeometry(m),m.isInstancedBufferGeometry===!0&&delete m._maxInstanceCount,t.memory.geometries--}function c(p,m){return i[m.id]===!0||(m.addEventListener("dispose",l),i[m.id]=!0,t.memory.geometries++),m}function u(p){const m=p.attributes;for(const y in m)e.update(m[y],r.ARRAY_BUFFER);const g=p.morphAttributes;for(const y in g){const M=g[y];for(let x=0,_=M.length;x<_;x++)e.update(M[x],r.ARRAY_BUFFER)}}function h(p){const m=[],g=p.index,y=p.attributes.position;let M=0;if(g!==null){const w=g.array;M=g.version;for(let E=0,T=w.length;E<T;E+=3){const U=w[E+0],P=w[E+1],D=w[E+2];m.push(U,P,P,D,D,U)}}else if(y!==void 0){const w=y.array;M=y.version;for(let E=0,T=w.length/3-1;E<T;E+=3){const U=E+0,P=E+1,D=E+2;m.push(U,P,P,D,D,U)}}else return;const x=new(y_(m)?vp:gp)(m,1);x.version=M;const _=s.get(p);_&&e.remove(_),s.set(p,x)}function f(p){const m=s.get(p);if(m){const g=p.index;g!==null&&m.version<g.version&&h(p)}else h(p);return s.get(p)}return{get:c,update:u,getWireframeAttribute:f}}function r1(r,e,t){let n;function i(m){n=m}let s,l;function c(m){s=m.type,l=m.bytesPerElement}function u(m,g){r.drawElements(n,g,s,m*l),t.update(g,n,1)}function h(m,g,y){y!==0&&(r.drawElementsInstanced(n,g,s,m*l,y),t.update(g,n,y))}function f(m,g,y){if(y===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(n,g,0,s,m,0,y);let x=0;for(let _=0;_<y;_++)x+=g[_];t.update(x,n,1)}function p(m,g,y,M){if(y===0)return;const x=e.get("WEBGL_multi_draw");if(x===null)for(let _=0;_<m.length;_++)h(m[_]/l,g[_],M[_]);else{x.multiDrawElementsInstancedWEBGL(n,g,0,s,m,0,M,0,y);let _=0;for(let w=0;w<y;w++)_+=g[w]*M[w];t.update(_,n,1)}}this.setMode=i,this.setIndex=c,this.render=u,this.renderInstances=h,this.renderMultiDraw=f,this.renderMultiDrawInstances=p}function s1(r){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function n(s,l,c){switch(t.calls++,l){case r.TRIANGLES:t.triangles+=c*(s/3);break;case r.LINES:t.lines+=c*(s/2);break;case r.LINE_STRIP:t.lines+=c*(s-1);break;case r.LINE_LOOP:t.lines+=c*s;break;case r.POINTS:t.points+=c*s;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",l);break}}function i(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:i,update:n}}function o1(r,e,t){const n=new WeakMap,i=new At;function s(l,c,u){const h=l.morphTargetInfluences,f=c.morphAttributes.position||c.morphAttributes.normal||c.morphAttributes.color,p=f!==void 0?f.length:0;let m=n.get(c);if(m===void 0||m.count!==p){let C=function(){D.dispose(),n.delete(c),c.removeEventListener("dispose",C)};m!==void 0&&m.texture.dispose();const g=c.morphAttributes.position!==void 0,y=c.morphAttributes.normal!==void 0,M=c.morphAttributes.color!==void 0,x=c.morphAttributes.position||[],_=c.morphAttributes.normal||[],w=c.morphAttributes.color||[];let E=0;g===!0&&(E=1),y===!0&&(E=2),M===!0&&(E=3);let T=c.attributes.position.count*E,U=1;T>e.maxTextureSize&&(U=Math.ceil(T/e.maxTextureSize),T=e.maxTextureSize);const P=new Float32Array(T*U*4*p),D=new oh(P,T,U,p);D.type=Kn,D.needsUpdate=!0;const F=E*4;for(let b=0;b<p;b++){const N=x[b],q=_[b],Y=w[b],K=T*U*4*b;for(let le=0;le<N.count;le++){const $=le*F;g===!0&&(i.fromBufferAttribute(N,le),P[K+$+0]=i.x,P[K+$+1]=i.y,P[K+$+2]=i.z,P[K+$+3]=0),y===!0&&(i.fromBufferAttribute(q,le),P[K+$+4]=i.x,P[K+$+5]=i.y,P[K+$+6]=i.z,P[K+$+7]=0),M===!0&&(i.fromBufferAttribute(Y,le),P[K+$+8]=i.x,P[K+$+9]=i.y,P[K+$+10]=i.z,P[K+$+11]=Y.itemSize===4?i.w:1)}}m={count:p,texture:D,size:new ae(T,U)},n.set(c,m),c.addEventListener("dispose",C)}if(l.isInstancedMesh===!0&&l.morphTexture!==null)u.getUniforms().setValue(r,"morphTexture",l.morphTexture,t);else{let g=0;for(let M=0;M<h.length;M++)g+=h[M];const y=c.morphTargetsRelative?1:1-g;u.getUniforms().setValue(r,"morphTargetBaseInfluence",y),u.getUniforms().setValue(r,"morphTargetInfluences",h)}u.getUniforms().setValue(r,"morphTargetsTexture",m.texture,t),u.getUniforms().setValue(r,"morphTargetsTextureSize",m.size)}return{update:s}}function a1(r,e,t,n){let i=new WeakMap;function s(u){const h=n.render.frame,f=u.geometry,p=e.get(u,f);if(i.get(p)!==h&&(e.update(p),i.set(p,h)),u.isInstancedMesh&&(u.hasEventListener("dispose",c)===!1&&u.addEventListener("dispose",c),i.get(u)!==h&&(t.update(u.instanceMatrix,r.ARRAY_BUFFER),u.instanceColor!==null&&t.update(u.instanceColor,r.ARRAY_BUFFER),i.set(u,h))),u.isSkinnedMesh){const m=u.skeleton;i.get(m)!==h&&(m.update(),i.set(m,h))}return p}function l(){i=new WeakMap}function c(u){const h=u.target;h.removeEventListener("dispose",c),t.remove(h.instanceMatrix),h.instanceColor!==null&&t.remove(h.instanceColor)}return{update:s,dispose:l}}class yp extends Kt{constructor(e,t,n,i,s,l,c,u,h,f=As){if(f!==As&&f!==Ds)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");n===void 0&&f===As&&(n=yr),n===void 0&&f===Ds&&(n=Ls),super(null,i,s,l,c,u,f,n,h),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=c!==void 0?c:wn,this.minFilter=u!==void 0?u:wn,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}const C_=new Kt,e0=new yp(1,1),R_=new oh,P_=new mp,I_=new tl,t0=[],n0=[],i0=new Float32Array(16),r0=new Float32Array(9),s0=new Float32Array(4);function zo(r,e,t){const n=r[0];if(n<=0||n>0)return r;const i=e*t;let s=t0[i];if(s===void 0&&(s=new Float32Array(i),t0[i]=s),e!==0){n.toArray(s,0);for(let l=1,c=0;l!==e;++l)c+=t,r[l].toArray(s,c)}return s}function un(r,e){if(r.length!==e.length)return!1;for(let t=0,n=r.length;t<n;t++)if(r[t]!==e[t])return!1;return!0}function hn(r,e){for(let t=0,n=e.length;t<n;t++)r[t]=e[t]}function ah(r,e){let t=n0[e];t===void 0&&(t=new Int32Array(e),n0[e]=t);for(let n=0;n!==e;++n)t[n]=r.allocateTextureUnit();return t}function l1(r,e){const t=this.cache;t[0]!==e&&(r.uniform1f(this.addr,e),t[0]=e)}function c1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(r.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(un(t,e))return;r.uniform2fv(this.addr,e),hn(t,e)}}function u1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(r.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(r.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(un(t,e))return;r.uniform3fv(this.addr,e),hn(t,e)}}function h1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(r.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(un(t,e))return;r.uniform4fv(this.addr,e),hn(t,e)}}function f1(r,e){const t=this.cache,n=e.elements;if(n===void 0){if(un(t,e))return;r.uniformMatrix2fv(this.addr,!1,e),hn(t,e)}else{if(un(t,n))return;s0.set(n),r.uniformMatrix2fv(this.addr,!1,s0),hn(t,n)}}function d1(r,e){const t=this.cache,n=e.elements;if(n===void 0){if(un(t,e))return;r.uniformMatrix3fv(this.addr,!1,e),hn(t,e)}else{if(un(t,n))return;r0.set(n),r.uniformMatrix3fv(this.addr,!1,r0),hn(t,n)}}function p1(r,e){const t=this.cache,n=e.elements;if(n===void 0){if(un(t,e))return;r.uniformMatrix4fv(this.addr,!1,e),hn(t,e)}else{if(un(t,n))return;i0.set(n),r.uniformMatrix4fv(this.addr,!1,i0),hn(t,n)}}function m1(r,e){const t=this.cache;t[0]!==e&&(r.uniform1i(this.addr,e),t[0]=e)}function g1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(r.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(un(t,e))return;r.uniform2iv(this.addr,e),hn(t,e)}}function v1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(r.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(un(t,e))return;r.uniform3iv(this.addr,e),hn(t,e)}}function _1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(r.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(un(t,e))return;r.uniform4iv(this.addr,e),hn(t,e)}}function y1(r,e){const t=this.cache;t[0]!==e&&(r.uniform1ui(this.addr,e),t[0]=e)}function x1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(r.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(un(t,e))return;r.uniform2uiv(this.addr,e),hn(t,e)}}function S1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(r.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(un(t,e))return;r.uniform3uiv(this.addr,e),hn(t,e)}}function M1(r,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(r.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(un(t,e))return;r.uniform4uiv(this.addr,e),hn(t,e)}}function E1(r,e,t){const n=this.cache,i=t.allocateTextureUnit();n[0]!==i&&(r.uniform1i(this.addr,i),n[0]=i);let s;this.type===r.SAMPLER_2D_SHADOW?(e0.compareFunction=dp,s=e0):s=C_,t.setTexture2D(e||s,i)}function w1(r,e,t){const n=this.cache,i=t.allocateTextureUnit();n[0]!==i&&(r.uniform1i(this.addr,i),n[0]=i),t.setTexture3D(e||P_,i)}function T1(r,e,t){const n=this.cache,i=t.allocateTextureUnit();n[0]!==i&&(r.uniform1i(this.addr,i),n[0]=i),t.setTextureCube(e||I_,i)}function A1(r,e,t){const n=this.cache,i=t.allocateTextureUnit();n[0]!==i&&(r.uniform1i(this.addr,i),n[0]=i),t.setTexture2DArray(e||R_,i)}function b1(r){switch(r){case 5126:return l1;case 35664:return c1;case 35665:return u1;case 35666:return h1;case 35674:return f1;case 35675:return d1;case 35676:return p1;case 5124:case 35670:return m1;case 35667:case 35671:return g1;case 35668:case 35672:return v1;case 35669:case 35673:return _1;case 5125:return y1;case 36294:return x1;case 36295:return S1;case 36296:return M1;case 35678:case 36198:case 36298:case 36306:case 35682:return E1;case 35679:case 36299:case 36307:return w1;case 35680:case 36300:case 36308:case 36293:return T1;case 36289:case 36303:case 36311:case 36292:return A1}}function C1(r,e){r.uniform1fv(this.addr,e)}function R1(r,e){const t=zo(e,this.size,2);r.uniform2fv(this.addr,t)}function P1(r,e){const t=zo(e,this.size,3);r.uniform3fv(this.addr,t)}function I1(r,e){const t=zo(e,this.size,4);r.uniform4fv(this.addr,t)}function L1(r,e){const t=zo(e,this.size,4);r.uniformMatrix2fv(this.addr,!1,t)}function D1(r,e){const t=zo(e,this.size,9);r.uniformMatrix3fv(this.addr,!1,t)}function U1(r,e){const t=zo(e,this.size,16);r.uniformMatrix4fv(this.addr,!1,t)}function N1(r,e){r.uniform1iv(this.addr,e)}function O1(r,e){r.uniform2iv(this.addr,e)}function F1(r,e){r.uniform3iv(this.addr,e)}function B1(r,e){r.uniform4iv(this.addr,e)}function z1(r,e){r.uniform1uiv(this.addr,e)}function k1(r,e){r.uniform2uiv(this.addr,e)}function H1(r,e){r.uniform3uiv(this.addr,e)}function V1(r,e){r.uniform4uiv(this.addr,e)}function G1(r,e,t){const n=this.cache,i=e.length,s=ah(t,i);un(n,s)||(r.uniform1iv(this.addr,s),hn(n,s));for(let l=0;l!==i;++l)t.setTexture2D(e[l]||C_,s[l])}function W1(r,e,t){const n=this.cache,i=e.length,s=ah(t,i);un(n,s)||(r.uniform1iv(this.addr,s),hn(n,s));for(let l=0;l!==i;++l)t.setTexture3D(e[l]||P_,s[l])}function X1(r,e,t){const n=this.cache,i=e.length,s=ah(t,i);un(n,s)||(r.uniform1iv(this.addr,s),hn(n,s));for(let l=0;l!==i;++l)t.setTextureCube(e[l]||I_,s[l])}function Y1(r,e,t){const n=this.cache,i=e.length,s=ah(t,i);un(n,s)||(r.uniform1iv(this.addr,s),hn(n,s));for(let l=0;l!==i;++l)t.setTexture2DArray(e[l]||R_,s[l])}function q1(r){switch(r){case 5126:return C1;case 35664:return R1;case 35665:return P1;case 35666:return I1;case 35674:return L1;case 35675:return D1;case 35676:return U1;case 5124:case 35670:return N1;case 35667:case 35671:return O1;case 35668:case 35672:return F1;case 35669:case 35673:return B1;case 5125:return z1;case 36294:return k1;case 36295:return H1;case 36296:return V1;case 35678:case 36198:case 36298:case 36306:case 35682:return G1;case 35679:case 36299:case 36307:return W1;case 35680:case 36300:case 36308:case 36293:return X1;case 36289:case 36303:case 36311:case 36292:return Y1}}class Z1{constructor(e,t,n){this.id=e,this.addr=n,this.cache=[],this.type=t.type,this.setValue=b1(t.type)}}class j1{constructor(e,t,n){this.id=e,this.addr=n,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=q1(t.type)}}class J1{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,n){const i=this.seq;for(let s=0,l=i.length;s!==l;++s){const c=i[s];c.setValue(e,t[c.id],n)}}}const od=/(\w+)(\])?(\[|\.)?/g;function o0(r,e){r.seq.push(e),r.map[e.id]=e}function K1(r,e,t){const n=r.name,i=n.length;for(od.lastIndex=0;;){const s=od.exec(n),l=od.lastIndex;let c=s[1];const u=s[2]==="]",h=s[3];if(u&&(c=c|0),h===void 0||h==="["&&l+2===i){o0(t,h===void 0?new Z1(c,r,e):new j1(c,r,e));break}else{let p=t.map[c];p===void 0&&(p=new J1(c),o0(t,p)),t=p}}}class au{constructor(e,t){this.seq=[],this.map={};const n=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let i=0;i<n;++i){const s=e.getActiveUniform(t,i),l=e.getUniformLocation(t,s.name);K1(s,l,this)}}setValue(e,t,n,i){const s=this.map[t];s!==void 0&&s.setValue(e,n,i)}setOptional(e,t,n){const i=t[n];i!==void 0&&this.setValue(e,n,i)}static upload(e,t,n,i){for(let s=0,l=t.length;s!==l;++s){const c=t[s],u=n[c.id];u.needsUpdate!==!1&&c.setValue(e,u.value,i)}}static seqWithValue(e,t){const n=[];for(let i=0,s=e.length;i!==s;++i){const l=e[i];l.id in t&&n.push(l)}return n}}function a0(r,e,t){const n=r.createShader(e);return r.shaderSource(n,t),r.compileShader(n),n}const Q1=37297;let $1=0;function eT(r,e){const t=r.split(`
`),n=[],i=Math.max(e-6,0),s=Math.min(e+6,t.length);for(let l=i;l<s;l++){const c=l+1;n.push(`${c===e?">":" "} ${c}: ${t[l]}`)}return n.join(`
`)}const l0=new gt;function tT(r){Pt._getMatrix(l0,Pt.workingColorSpace,r);const e=`mat3( ${l0.elements.map(t=>t.toFixed(4))} )`;switch(Pt.getTransfer(r)){case $a:return[e,"LinearTransferOETF"];case Ft:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",r),[e,"LinearTransferOETF"]}}function c0(r,e,t){const n=r.getShaderParameter(e,r.COMPILE_STATUS),i=r.getShaderInfoLog(e).trim();if(n&&i==="")return"";const s=/ERROR: 0:(\d+)/.exec(i);if(s){const l=parseInt(s[1]);return t.toUpperCase()+`

`+i+`

`+eT(r.getShaderSource(e),l)}else return i}function nT(r,e){const t=tT(e);return[`vec4 ${r}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function iT(r,e){let t;switch(e){case Qv:t="Linear";break;case $v:t="Reinhard";break;case e_:t="Cineon";break;case tp:t="ACESFilmic";break;case n_:t="AgX";break;case i_:t="Neutral";break;case t_:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+r+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const Cc=new L;function rT(){Pt.getLuminanceCoefficients(Cc);const r=Cc.x.toFixed(4),e=Cc.y.toFixed(4),t=Cc.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${r}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function sT(r){return[r.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",r.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Ma).join(`
`)}function oT(r){const e=[];for(const t in r){const n=r[t];n!==!1&&e.push("#define "+t+" "+n)}return e.join(`
`)}function aT(r,e){const t={},n=r.getProgramParameter(e,r.ACTIVE_ATTRIBUTES);for(let i=0;i<n;i++){const s=r.getActiveAttrib(e,i),l=s.name;let c=1;s.type===r.FLOAT_MAT2&&(c=2),s.type===r.FLOAT_MAT3&&(c=3),s.type===r.FLOAT_MAT4&&(c=4),t[l]={type:s.type,location:r.getAttribLocation(e,l),locationSize:c}}return t}function Ma(r){return r!==""}function u0(r,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return r.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function h0(r,e){return r.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const lT=/^[ \t]*#include +<([\w\d./]+)>/gm;function Wd(r){return r.replace(lT,uT)}const cT=new Map;function uT(r,e){let t=yt[e];if(t===void 0){const n=cT.get(e);if(n!==void 0)t=yt[n],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,n);else throw new Error("Can not resolve #include <"+e+">")}return Wd(t)}const hT=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function f0(r){return r.replace(hT,fT)}function fT(r,e,t,n){let i="";for(let s=parseInt(e);s<parseInt(t);s++)i+=n.replace(/\[\s*i\s*\]/g,"[ "+s+" ]").replace(/UNROLLED_LOOP_INDEX/g,s);return i}function d0(r){let e=`precision ${r.precision} float;
	precision ${r.precision} int;
	precision ${r.precision} sampler2D;
	precision ${r.precision} samplerCube;
	precision ${r.precision} sampler3D;
	precision ${r.precision} sampler2DArray;
	precision ${r.precision} sampler2DShadow;
	precision ${r.precision} samplerCubeShadow;
	precision ${r.precision} sampler2DArrayShadow;
	precision ${r.precision} isampler2D;
	precision ${r.precision} isampler3D;
	precision ${r.precision} isamplerCube;
	precision ${r.precision} isampler2DArray;
	precision ${r.precision} usampler2D;
	precision ${r.precision} usampler3D;
	precision ${r.precision} usamplerCube;
	precision ${r.precision} usampler2DArray;
	`;return r.precision==="highp"?e+=`
#define HIGH_PRECISION`:r.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:r.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}function dT(r){let e="SHADOWMAP_TYPE_BASIC";return r.shadowMapType===Ku?e="SHADOWMAP_TYPE_PCF":r.shadowMapType===Ea?e="SHADOWMAP_TYPE_PCF_SOFT":r.shadowMapType===wi&&(e="SHADOWMAP_TYPE_VSM"),e}function pT(r){let e="ENVMAP_TYPE_CUBE";if(r.envMap)switch(r.envMapMode){case _r:case Hr:e="ENVMAP_TYPE_CUBE";break;case Oo:e="ENVMAP_TYPE_CUBE_UV";break}return e}function mT(r){let e="ENVMAP_MODE_REFLECTION";if(r.envMap)switch(r.envMapMode){case Hr:e="ENVMAP_MODE_REFRACTION";break}return e}function gT(r){let e="ENVMAP_BLENDING_NONE";if(r.envMap)switch(r.combine){case Ka:e="ENVMAP_BLENDING_MULTIPLY";break;case Jv:e="ENVMAP_BLENDING_MIX";break;case Kv:e="ENVMAP_BLENDING_ADD";break}return e}function vT(r){const e=r.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,n=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),7*16)),texelHeight:n,maxMip:t}}function _T(r,e,t,n){const i=r.getContext(),s=t.defines;let l=t.vertexShader,c=t.fragmentShader;const u=dT(t),h=pT(t),f=mT(t),p=gT(t),m=vT(t),g=sT(t),y=oT(s),M=i.createProgram();let x,_,w=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(x=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,y].filter(Ma).join(`
`),x.length>0&&(x+=`
`),_=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,y].filter(Ma).join(`
`),_.length>0&&(_+=`
`)):(x=[d0(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,y,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+f:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+u:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Ma).join(`
`),_=[d0(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,y,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+h:"",t.envMap?"#define "+f:"",t.envMap?"#define "+p:"",m?"#define CUBEUV_TEXEL_WIDTH "+m.texelWidth:"",m?"#define CUBEUV_TEXEL_HEIGHT "+m.texelHeight:"",m?"#define CUBEUV_MAX_MIP "+m.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+u:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==qi?"#define TONE_MAPPING":"",t.toneMapping!==qi?yt.tonemapping_pars_fragment:"",t.toneMapping!==qi?iT("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",yt.colorspace_pars_fragment,nT("linearToOutputTexel",t.outputColorSpace),rT(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Ma).join(`
`)),l=Wd(l),l=u0(l,t),l=h0(l,t),c=Wd(c),c=u0(c,t),c=h0(c,t),l=f0(l),c=f0(c),t.isRawShaderMaterial!==!0&&(w=`#version 300 es
`,x=[g,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+x,_=["#define varying in",t.glslVersion===Vd?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===Vd?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+_);const E=w+x+l,T=w+_+c,U=a0(i,i.VERTEX_SHADER,E),P=a0(i,i.FRAGMENT_SHADER,T);i.attachShader(M,U),i.attachShader(M,P),t.index0AttributeName!==void 0?i.bindAttribLocation(M,0,t.index0AttributeName):t.morphTargets===!0&&i.bindAttribLocation(M,0,"position"),i.linkProgram(M);function D(N){if(r.debug.checkShaderErrors){const q=i.getProgramInfoLog(M).trim(),Y=i.getShaderInfoLog(U).trim(),K=i.getShaderInfoLog(P).trim();let le=!0,$=!0;if(i.getProgramParameter(M,i.LINK_STATUS)===!1)if(le=!1,typeof r.debug.onShaderError=="function")r.debug.onShaderError(i,M,U,P);else{const pe=c0(i,U,"vertex"),J=c0(i,P,"fragment");console.error("THREE.WebGLProgram: Shader Error "+i.getError()+" - VALIDATE_STATUS "+i.getProgramParameter(M,i.VALIDATE_STATUS)+`

Material Name: `+N.name+`
Material Type: `+N.type+`

Program Info Log: `+q+`
`+pe+`
`+J)}else q!==""?console.warn("THREE.WebGLProgram: Program Info Log:",q):(Y===""||K==="")&&($=!1);$&&(N.diagnostics={runnable:le,programLog:q,vertexShader:{log:Y,prefix:x},fragmentShader:{log:K,prefix:_}})}i.deleteShader(U),i.deleteShader(P),F=new au(i,M),C=aT(i,M)}let F;this.getUniforms=function(){return F===void 0&&D(this),F};let C;this.getAttributes=function(){return C===void 0&&D(this),C};let b=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return b===!1&&(b=i.getProgramParameter(M,Q1)),b},this.destroy=function(){n.releaseStatesOfProgram(this),i.deleteProgram(M),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=$1++,this.cacheKey=e,this.usedTimes=1,this.program=M,this.vertexShader=U,this.fragmentShader=P,this}let yT=0;class xT{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,n=e.fragmentShader,i=this._getShaderStage(t),s=this._getShaderStage(n),l=this._getShaderCacheForMaterial(e);return l.has(i)===!1&&(l.add(i),i.usedTimes++),l.has(s)===!1&&(l.add(s),s.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const n of t)n.usedTimes--,n.usedTimes===0&&this.shaderCache.delete(n.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let n=t.get(e);return n===void 0&&(n=new Set,t.set(e,n)),n}_getShaderStage(e){const t=this.shaderCache;let n=t.get(e);return n===void 0&&(n=new ST(e),t.set(e,n)),n}}class ST{constructor(e){this.id=yT++,this.code=e,this.usedTimes=0}}function MT(r,e,t,n,i,s,l){const c=new Cs,u=new xT,h=new Set,f=[],p=i.logarithmicDepthBuffer,m=i.vertexTextures;let g=i.precision;const y={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function M(C){return h.add(C),C===0?"uv":`uv${C}`}function x(C,b,N,q,Y){const K=q.fog,le=Y.geometry,$=C.isMeshStandardMaterial?q.environment:null,pe=(C.isMeshStandardMaterial?t:e).get(C.envMap||$),J=pe&&pe.mapping===Oo?pe.image.height:null,xe=y[C.type];C.precision!==null&&(g=i.getMaxPrecision(C.precision),g!==C.precision&&console.warn("THREE.WebGLProgram.getParameters:",C.precision,"not supported, using",g,"instead."));const me=le.morphAttributes.position||le.morphAttributes.normal||le.morphAttributes.color,Se=me!==void 0?me.length:0;let Qe=0;le.morphAttributes.position!==void 0&&(Qe=1),le.morphAttributes.normal!==void 0&&(Qe=2),le.morphAttributes.color!==void 0&&(Qe=3);let Je,se,ge,Ve;if(xe){const bt=Ai[xe];Je=bt.vertexShader,se=bt.fragmentShader}else Je=C.vertexShader,se=C.fragmentShader,u.update(C),ge=u.getVertexShaderID(C),Ve=u.getFragmentShaderID(C);const we=r.getRenderTarget(),et=r.state.buffers.depth.getReversed(),lt=Y.isInstancedMesh===!0,tt=Y.isBatchedMesh===!0,ft=!!C.map,he=!!C.matcap,de=!!pe,z=!!C.aoMap,je=!!C.lightMap,ve=!!C.bumpMap,Oe=!!C.normalMap,Te=!!C.displacementMap,it=!!C.emissiveMap,Pe=!!C.metalnessMap,O=!!C.roughnessMap,R=C.anisotropy>0,Z=C.clearcoat>0,re=C.dispersion>0,fe=C.iridescence>0,ce=C.sheen>0,We=C.transmission>0,Ae=R&&!!C.anisotropyMap,Fe=Z&&!!C.clearcoatMap,St=Z&&!!C.clearcoatNormalMap,_e=Z&&!!C.clearcoatRoughnessMap,He=fe&&!!C.iridescenceMap,rt=fe&&!!C.iridescenceThicknessMap,ct=ce&&!!C.sheenColorMap,ze=ce&&!!C.sheenRoughnessMap,H=!!C.specularMap,oe=!!C.specularColorMap,Re=!!C.specularIntensityMap,k=We&&!!C.transmissionMap,ye=We&&!!C.thicknessMap,te=!!C.gradientMap,ue=!!C.alphaMap,Ue=C.alphaTest>0,Ce=!!C.alphaHash,nt=!!C.extensions;let It=qi;C.toneMapped&&(we===null||we.isXRRenderTarget===!0)&&(It=r.toneMapping);const Ht={shaderID:xe,shaderType:C.type,shaderName:C.name,vertexShader:Je,fragmentShader:se,defines:C.defines,customVertexShaderID:ge,customFragmentShaderID:Ve,isRawShaderMaterial:C.isRawShaderMaterial===!0,glslVersion:C.glslVersion,precision:g,batching:tt,batchingColor:tt&&Y._colorsTexture!==null,instancing:lt,instancingColor:lt&&Y.instanceColor!==null,instancingMorph:lt&&Y.morphTexture!==null,supportsVertexTextures:m,outputColorSpace:we===null?r.outputColorSpace:we.isXRRenderTarget===!0?we.texture.colorSpace:Ns,alphaToCoverage:!!C.alphaToCoverage,map:ft,matcap:he,envMap:de,envMapMode:de&&pe.mapping,envMapCubeUVHeight:J,aoMap:z,lightMap:je,bumpMap:ve,normalMap:Oe,displacementMap:m&&Te,emissiveMap:it,normalMapObjectSpace:Oe&&C.normalMapType===u_,normalMapTangentSpace:Oe&&C.normalMapType===Gr,metalnessMap:Pe,roughnessMap:O,anisotropy:R,anisotropyMap:Ae,clearcoat:Z,clearcoatMap:Fe,clearcoatNormalMap:St,clearcoatRoughnessMap:_e,dispersion:re,iridescence:fe,iridescenceMap:He,iridescenceThicknessMap:rt,sheen:ce,sheenColorMap:ct,sheenRoughnessMap:ze,specularMap:H,specularColorMap:oe,specularIntensityMap:Re,transmission:We,transmissionMap:k,thicknessMap:ye,gradientMap:te,opaque:C.transparent===!1&&C.blending===Ts&&C.alphaToCoverage===!1,alphaMap:ue,alphaTest:Ue,alphaHash:Ce,combine:C.combine,mapUv:ft&&M(C.map.channel),aoMapUv:z&&M(C.aoMap.channel),lightMapUv:je&&M(C.lightMap.channel),bumpMapUv:ve&&M(C.bumpMap.channel),normalMapUv:Oe&&M(C.normalMap.channel),displacementMapUv:Te&&M(C.displacementMap.channel),emissiveMapUv:it&&M(C.emissiveMap.channel),metalnessMapUv:Pe&&M(C.metalnessMap.channel),roughnessMapUv:O&&M(C.roughnessMap.channel),anisotropyMapUv:Ae&&M(C.anisotropyMap.channel),clearcoatMapUv:Fe&&M(C.clearcoatMap.channel),clearcoatNormalMapUv:St&&M(C.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:_e&&M(C.clearcoatRoughnessMap.channel),iridescenceMapUv:He&&M(C.iridescenceMap.channel),iridescenceThicknessMapUv:rt&&M(C.iridescenceThicknessMap.channel),sheenColorMapUv:ct&&M(C.sheenColorMap.channel),sheenRoughnessMapUv:ze&&M(C.sheenRoughnessMap.channel),specularMapUv:H&&M(C.specularMap.channel),specularColorMapUv:oe&&M(C.specularColorMap.channel),specularIntensityMapUv:Re&&M(C.specularIntensityMap.channel),transmissionMapUv:k&&M(C.transmissionMap.channel),thicknessMapUv:ye&&M(C.thicknessMap.channel),alphaMapUv:ue&&M(C.alphaMap.channel),vertexTangents:!!le.attributes.tangent&&(Oe||R),vertexColors:C.vertexColors,vertexAlphas:C.vertexColors===!0&&!!le.attributes.color&&le.attributes.color.itemSize===4,pointsUvs:Y.isPoints===!0&&!!le.attributes.uv&&(ft||ue),fog:!!K,useFog:C.fog===!0,fogExp2:!!K&&K.isFogExp2,flatShading:C.flatShading===!0,sizeAttenuation:C.sizeAttenuation===!0,logarithmicDepthBuffer:p,reverseDepthBuffer:et,skinning:Y.isSkinnedMesh===!0,morphTargets:le.morphAttributes.position!==void 0,morphNormals:le.morphAttributes.normal!==void 0,morphColors:le.morphAttributes.color!==void 0,morphTargetsCount:Se,morphTextureStride:Qe,numDirLights:b.directional.length,numPointLights:b.point.length,numSpotLights:b.spot.length,numSpotLightMaps:b.spotLightMap.length,numRectAreaLights:b.rectArea.length,numHemiLights:b.hemi.length,numDirLightShadows:b.directionalShadowMap.length,numPointLightShadows:b.pointShadowMap.length,numSpotLightShadows:b.spotShadowMap.length,numSpotLightShadowsWithMaps:b.numSpotLightShadowsWithMaps,numLightProbes:b.numLightProbes,numClippingPlanes:l.numPlanes,numClipIntersection:l.numIntersection,dithering:C.dithering,shadowMapEnabled:r.shadowMap.enabled&&N.length>0,shadowMapType:r.shadowMap.type,toneMapping:It,decodeVideoTexture:ft&&C.map.isVideoTexture===!0&&Pt.getTransfer(C.map.colorSpace)===Ft,decodeVideoTextureEmissive:it&&C.emissiveMap.isVideoTexture===!0&&Pt.getTransfer(C.emissiveMap.colorSpace)===Ft,premultipliedAlpha:C.premultipliedAlpha,doubleSided:C.side===Gi,flipSided:C.side===Vn,useDepthPacking:C.depthPacking>=0,depthPacking:C.depthPacking||0,index0AttributeName:C.index0AttributeName,extensionClipCullDistance:nt&&C.extensions.clipCullDistance===!0&&n.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(nt&&C.extensions.multiDraw===!0||tt)&&n.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:n.has("KHR_parallel_shader_compile"),customProgramCacheKey:C.customProgramCacheKey()};return Ht.vertexUv1s=h.has(1),Ht.vertexUv2s=h.has(2),Ht.vertexUv3s=h.has(3),h.clear(),Ht}function _(C){const b=[];if(C.shaderID?b.push(C.shaderID):(b.push(C.customVertexShaderID),b.push(C.customFragmentShaderID)),C.defines!==void 0)for(const N in C.defines)b.push(N),b.push(C.defines[N]);return C.isRawShaderMaterial===!1&&(w(b,C),E(b,C),b.push(r.outputColorSpace)),b.push(C.customProgramCacheKey),b.join()}function w(C,b){C.push(b.precision),C.push(b.outputColorSpace),C.push(b.envMapMode),C.push(b.envMapCubeUVHeight),C.push(b.mapUv),C.push(b.alphaMapUv),C.push(b.lightMapUv),C.push(b.aoMapUv),C.push(b.bumpMapUv),C.push(b.normalMapUv),C.push(b.displacementMapUv),C.push(b.emissiveMapUv),C.push(b.metalnessMapUv),C.push(b.roughnessMapUv),C.push(b.anisotropyMapUv),C.push(b.clearcoatMapUv),C.push(b.clearcoatNormalMapUv),C.push(b.clearcoatRoughnessMapUv),C.push(b.iridescenceMapUv),C.push(b.iridescenceThicknessMapUv),C.push(b.sheenColorMapUv),C.push(b.sheenRoughnessMapUv),C.push(b.specularMapUv),C.push(b.specularColorMapUv),C.push(b.specularIntensityMapUv),C.push(b.transmissionMapUv),C.push(b.thicknessMapUv),C.push(b.combine),C.push(b.fogExp2),C.push(b.sizeAttenuation),C.push(b.morphTargetsCount),C.push(b.morphAttributeCount),C.push(b.numDirLights),C.push(b.numPointLights),C.push(b.numSpotLights),C.push(b.numSpotLightMaps),C.push(b.numHemiLights),C.push(b.numRectAreaLights),C.push(b.numDirLightShadows),C.push(b.numPointLightShadows),C.push(b.numSpotLightShadows),C.push(b.numSpotLightShadowsWithMaps),C.push(b.numLightProbes),C.push(b.shadowMapType),C.push(b.toneMapping),C.push(b.numClippingPlanes),C.push(b.numClipIntersection),C.push(b.depthPacking)}function E(C,b){c.disableAll(),b.supportsVertexTextures&&c.enable(0),b.instancing&&c.enable(1),b.instancingColor&&c.enable(2),b.instancingMorph&&c.enable(3),b.matcap&&c.enable(4),b.envMap&&c.enable(5),b.normalMapObjectSpace&&c.enable(6),b.normalMapTangentSpace&&c.enable(7),b.clearcoat&&c.enable(8),b.iridescence&&c.enable(9),b.alphaTest&&c.enable(10),b.vertexColors&&c.enable(11),b.vertexAlphas&&c.enable(12),b.vertexUv1s&&c.enable(13),b.vertexUv2s&&c.enable(14),b.vertexUv3s&&c.enable(15),b.vertexTangents&&c.enable(16),b.anisotropy&&c.enable(17),b.alphaHash&&c.enable(18),b.batching&&c.enable(19),b.dispersion&&c.enable(20),b.batchingColor&&c.enable(21),C.push(c.mask),c.disableAll(),b.fog&&c.enable(0),b.useFog&&c.enable(1),b.flatShading&&c.enable(2),b.logarithmicDepthBuffer&&c.enable(3),b.reverseDepthBuffer&&c.enable(4),b.skinning&&c.enable(5),b.morphTargets&&c.enable(6),b.morphNormals&&c.enable(7),b.morphColors&&c.enable(8),b.premultipliedAlpha&&c.enable(9),b.shadowMapEnabled&&c.enable(10),b.doubleSided&&c.enable(11),b.flipSided&&c.enable(12),b.useDepthPacking&&c.enable(13),b.dithering&&c.enable(14),b.transmission&&c.enable(15),b.sheen&&c.enable(16),b.opaque&&c.enable(17),b.pointsUvs&&c.enable(18),b.decodeVideoTexture&&c.enable(19),b.decodeVideoTextureEmissive&&c.enable(20),b.alphaToCoverage&&c.enable(21),C.push(c.mask)}function T(C){const b=y[C.type];let N;if(b){const q=Ai[b];N=Xu.clone(q.uniforms)}else N=C.uniforms;return N}function U(C,b){let N;for(let q=0,Y=f.length;q<Y;q++){const K=f[q];if(K.cacheKey===b){N=K,++N.usedTimes;break}}return N===void 0&&(N=new _T(r,b,C,s),f.push(N)),N}function P(C){if(--C.usedTimes===0){const b=f.indexOf(C);f[b]=f[f.length-1],f.pop(),C.destroy()}}function D(C){u.remove(C)}function F(){u.dispose()}return{getParameters:x,getProgramCacheKey:_,getUniforms:T,acquireProgram:U,releaseProgram:P,releaseShaderCache:D,programs:f,dispose:F}}function ET(){let r=new WeakMap;function e(l){return r.has(l)}function t(l){let c=r.get(l);return c===void 0&&(c={},r.set(l,c)),c}function n(l){r.delete(l)}function i(l,c,u){r.get(l)[c]=u}function s(){r=new WeakMap}return{has:e,get:t,remove:n,update:i,dispose:s}}function wT(r,e){return r.groupOrder!==e.groupOrder?r.groupOrder-e.groupOrder:r.renderOrder!==e.renderOrder?r.renderOrder-e.renderOrder:r.material.id!==e.material.id?r.material.id-e.material.id:r.z!==e.z?r.z-e.z:r.id-e.id}function p0(r,e){return r.groupOrder!==e.groupOrder?r.groupOrder-e.groupOrder:r.renderOrder!==e.renderOrder?r.renderOrder-e.renderOrder:r.z!==e.z?e.z-r.z:r.id-e.id}function m0(){const r=[];let e=0;const t=[],n=[],i=[];function s(){e=0,t.length=0,n.length=0,i.length=0}function l(p,m,g,y,M,x){let _=r[e];return _===void 0?(_={id:p.id,object:p,geometry:m,material:g,groupOrder:y,renderOrder:p.renderOrder,z:M,group:x},r[e]=_):(_.id=p.id,_.object=p,_.geometry=m,_.material=g,_.groupOrder=y,_.renderOrder=p.renderOrder,_.z=M,_.group=x),e++,_}function c(p,m,g,y,M,x){const _=l(p,m,g,y,M,x);g.transmission>0?n.push(_):g.transparent===!0?i.push(_):t.push(_)}function u(p,m,g,y,M,x){const _=l(p,m,g,y,M,x);g.transmission>0?n.unshift(_):g.transparent===!0?i.unshift(_):t.unshift(_)}function h(p,m){t.length>1&&t.sort(p||wT),n.length>1&&n.sort(m||p0),i.length>1&&i.sort(m||p0)}function f(){for(let p=e,m=r.length;p<m;p++){const g=r[p];if(g.id===null)break;g.id=null,g.object=null,g.geometry=null,g.material=null,g.group=null}}return{opaque:t,transmissive:n,transparent:i,init:s,push:c,unshift:u,finish:f,sort:h}}function TT(){let r=new WeakMap;function e(n,i){const s=r.get(n);let l;return s===void 0?(l=new m0,r.set(n,[l])):i>=s.length?(l=new m0,s.push(l)):l=s[i],l}function t(){r=new WeakMap}return{get:e,dispose:t}}function AT(){const r={};return{get:function(e){if(r[e.id]!==void 0)return r[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new L,color:new Be};break;case"SpotLight":t={position:new L,direction:new L,color:new Be,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new L,color:new Be,distance:0,decay:0};break;case"HemisphereLight":t={direction:new L,skyColor:new Be,groundColor:new Be};break;case"RectAreaLight":t={color:new Be,position:new L,halfWidth:new L,halfHeight:new L};break}return r[e.id]=t,t}}}function bT(){const r={};return{get:function(e){if(r[e.id]!==void 0)return r[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ae};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ae};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ae,shadowCameraNear:1,shadowCameraFar:1e3};break}return r[e.id]=t,t}}}let CT=0;function RT(r,e){return(e.castShadow?2:0)-(r.castShadow?2:0)+(e.map?1:0)-(r.map?1:0)}function PT(r){const e=new AT,t=bT(),n={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let h=0;h<9;h++)n.probe.push(new L);const i=new L,s=new ut,l=new ut;function c(h){let f=0,p=0,m=0;for(let C=0;C<9;C++)n.probe[C].set(0,0,0);let g=0,y=0,M=0,x=0,_=0,w=0,E=0,T=0,U=0,P=0,D=0;h.sort(RT);for(let C=0,b=h.length;C<b;C++){const N=h[C],q=N.color,Y=N.intensity,K=N.distance,le=N.shadow&&N.shadow.map?N.shadow.map.texture:null;if(N.isAmbientLight)f+=q.r*Y,p+=q.g*Y,m+=q.b*Y;else if(N.isLightProbe){for(let $=0;$<9;$++)n.probe[$].addScaledVector(N.sh.coefficients[$],Y);D++}else if(N.isDirectionalLight){const $=e.get(N);if($.color.copy(N.color).multiplyScalar(N.intensity),N.castShadow){const pe=N.shadow,J=t.get(N);J.shadowIntensity=pe.intensity,J.shadowBias=pe.bias,J.shadowNormalBias=pe.normalBias,J.shadowRadius=pe.radius,J.shadowMapSize=pe.mapSize,n.directionalShadow[g]=J,n.directionalShadowMap[g]=le,n.directionalShadowMatrix[g]=N.shadow.matrix,w++}n.directional[g]=$,g++}else if(N.isSpotLight){const $=e.get(N);$.position.setFromMatrixPosition(N.matrixWorld),$.color.copy(q).multiplyScalar(Y),$.distance=K,$.coneCos=Math.cos(N.angle),$.penumbraCos=Math.cos(N.angle*(1-N.penumbra)),$.decay=N.decay,n.spot[M]=$;const pe=N.shadow;if(N.map&&(n.spotLightMap[U]=N.map,U++,pe.updateMatrices(N),N.castShadow&&P++),n.spotLightMatrix[M]=pe.matrix,N.castShadow){const J=t.get(N);J.shadowIntensity=pe.intensity,J.shadowBias=pe.bias,J.shadowNormalBias=pe.normalBias,J.shadowRadius=pe.radius,J.shadowMapSize=pe.mapSize,n.spotShadow[M]=J,n.spotShadowMap[M]=le,T++}M++}else if(N.isRectAreaLight){const $=e.get(N);$.color.copy(q).multiplyScalar(Y),$.halfWidth.set(N.width*.5,0,0),$.halfHeight.set(0,N.height*.5,0),n.rectArea[x]=$,x++}else if(N.isPointLight){const $=e.get(N);if($.color.copy(N.color).multiplyScalar(N.intensity),$.distance=N.distance,$.decay=N.decay,N.castShadow){const pe=N.shadow,J=t.get(N);J.shadowIntensity=pe.intensity,J.shadowBias=pe.bias,J.shadowNormalBias=pe.normalBias,J.shadowRadius=pe.radius,J.shadowMapSize=pe.mapSize,J.shadowCameraNear=pe.camera.near,J.shadowCameraFar=pe.camera.far,n.pointShadow[y]=J,n.pointShadowMap[y]=le,n.pointShadowMatrix[y]=N.shadow.matrix,E++}n.point[y]=$,y++}else if(N.isHemisphereLight){const $=e.get(N);$.skyColor.copy(N.color).multiplyScalar(Y),$.groundColor.copy(N.groundColor).multiplyScalar(Y),n.hemi[_]=$,_++}}x>0&&(r.has("OES_texture_float_linear")===!0?(n.rectAreaLTC1=be.LTC_FLOAT_1,n.rectAreaLTC2=be.LTC_FLOAT_2):(n.rectAreaLTC1=be.LTC_HALF_1,n.rectAreaLTC2=be.LTC_HALF_2)),n.ambient[0]=f,n.ambient[1]=p,n.ambient[2]=m;const F=n.hash;(F.directionalLength!==g||F.pointLength!==y||F.spotLength!==M||F.rectAreaLength!==x||F.hemiLength!==_||F.numDirectionalShadows!==w||F.numPointShadows!==E||F.numSpotShadows!==T||F.numSpotMaps!==U||F.numLightProbes!==D)&&(n.directional.length=g,n.spot.length=M,n.rectArea.length=x,n.point.length=y,n.hemi.length=_,n.directionalShadow.length=w,n.directionalShadowMap.length=w,n.pointShadow.length=E,n.pointShadowMap.length=E,n.spotShadow.length=T,n.spotShadowMap.length=T,n.directionalShadowMatrix.length=w,n.pointShadowMatrix.length=E,n.spotLightMatrix.length=T+U-P,n.spotLightMap.length=U,n.numSpotLightShadowsWithMaps=P,n.numLightProbes=D,F.directionalLength=g,F.pointLength=y,F.spotLength=M,F.rectAreaLength=x,F.hemiLength=_,F.numDirectionalShadows=w,F.numPointShadows=E,F.numSpotShadows=T,F.numSpotMaps=U,F.numLightProbes=D,n.version=CT++)}function u(h,f){let p=0,m=0,g=0,y=0,M=0;const x=f.matrixWorldInverse;for(let _=0,w=h.length;_<w;_++){const E=h[_];if(E.isDirectionalLight){const T=n.directional[p];T.direction.setFromMatrixPosition(E.matrixWorld),i.setFromMatrixPosition(E.target.matrixWorld),T.direction.sub(i),T.direction.transformDirection(x),p++}else if(E.isSpotLight){const T=n.spot[g];T.position.setFromMatrixPosition(E.matrixWorld),T.position.applyMatrix4(x),T.direction.setFromMatrixPosition(E.matrixWorld),i.setFromMatrixPosition(E.target.matrixWorld),T.direction.sub(i),T.direction.transformDirection(x),g++}else if(E.isRectAreaLight){const T=n.rectArea[y];T.position.setFromMatrixPosition(E.matrixWorld),T.position.applyMatrix4(x),l.identity(),s.copy(E.matrixWorld),s.premultiply(x),l.extractRotation(s),T.halfWidth.set(E.width*.5,0,0),T.halfHeight.set(0,E.height*.5,0),T.halfWidth.applyMatrix4(l),T.halfHeight.applyMatrix4(l),y++}else if(E.isPointLight){const T=n.point[m];T.position.setFromMatrixPosition(E.matrixWorld),T.position.applyMatrix4(x),m++}else if(E.isHemisphereLight){const T=n.hemi[M];T.direction.setFromMatrixPosition(E.matrixWorld),T.direction.transformDirection(x),M++}}}return{setup:c,setupView:u,state:n}}function g0(r){const e=new PT(r),t=[],n=[];function i(f){h.camera=f,t.length=0,n.length=0}function s(f){t.push(f)}function l(f){n.push(f)}function c(){e.setup(t)}function u(f){e.setupView(t,f)}const h={lightsArray:t,shadowsArray:n,camera:null,lights:e,transmissionRenderTarget:{}};return{init:i,state:h,setupLights:c,setupLightsView:u,pushLight:s,pushShadow:l}}function IT(r){let e=new WeakMap;function t(i,s=0){const l=e.get(i);let c;return l===void 0?(c=new g0(r),e.set(i,[c])):s>=l.length?(c=new g0(r),l.push(c)):c=l[s],c}function n(){e=new WeakMap}return{get:t,dispose:n}}class xp extends Nn{static get type(){return"MeshDepthMaterial"}constructor(e){super(),this.isMeshDepthMaterial=!0,this.depthPacking=l_,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Sp extends Nn{static get type(){return"MeshDistanceMaterial"}constructor(e){super(),this.isMeshDistanceMaterial=!0,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}const LT=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,DT=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
#include <packing>
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = unpackRGBATo2Half( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ) );
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = unpackRGBAToDepth( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ) );
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( squared_mean - mean * mean );
	gl_FragColor = pack2HalfToRGBA( vec2( mean, std_dev ) );
}`;function UT(r,e,t){let n=new nl;const i=new ae,s=new ae,l=new At,c=new xp({depthPacking:c_}),u=new Sp,h={},f=t.maxTextureSize,p={[vr]:Vn,[Vn]:vr,[Gi]:Gi},m=new _i({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new ae},radius:{value:4}},vertexShader:LT,fragmentShader:DT}),g=m.clone();g.defines.HORIZONTAL_PASS=1;const y=new xt;y.setAttribute("position",new zt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const M=new nn(y,m),x=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Ku;let _=this.type;this.render=function(P,D,F){if(x.enabled===!1||x.autoUpdate===!1&&x.needsUpdate===!1||P.length===0)return;const C=r.getRenderTarget(),b=r.getActiveCubeFace(),N=r.getActiveMipmapLevel(),q=r.state;q.setBlending(mr),q.buffers.color.setClear(1,1,1,1),q.buffers.depth.setTest(!0),q.setScissorTest(!1);const Y=_!==wi&&this.type===wi,K=_===wi&&this.type!==wi;for(let le=0,$=P.length;le<$;le++){const pe=P[le],J=pe.shadow;if(J===void 0){console.warn("THREE.WebGLShadowMap:",pe,"has no shadow.");continue}if(J.autoUpdate===!1&&J.needsUpdate===!1)continue;i.copy(J.mapSize);const xe=J.getFrameExtents();if(i.multiply(xe),s.copy(J.mapSize),(i.x>f||i.y>f)&&(i.x>f&&(s.x=Math.floor(f/xe.x),i.x=s.x*xe.x,J.mapSize.x=s.x),i.y>f&&(s.y=Math.floor(f/xe.y),i.y=s.y*xe.y,J.mapSize.y=s.y)),J.map===null||Y===!0||K===!0){const Se=this.type!==wi?{minFilter:wn,magFilter:wn}:{};J.map!==null&&J.map.dispose(),J.map=new Ci(i.x,i.y,Se),J.map.texture.name=pe.name+".shadowMap",J.camera.updateProjectionMatrix()}r.setRenderTarget(J.map),r.clear();const me=J.getViewportCount();for(let Se=0;Se<me;Se++){const Qe=J.getViewport(Se);l.set(s.x*Qe.x,s.y*Qe.y,s.x*Qe.z,s.y*Qe.w),q.viewport(l),J.updateMatrices(pe,Se),n=J.getFrustum(),T(D,F,J.camera,pe,this.type)}J.isPointLightShadow!==!0&&this.type===wi&&w(J,F),J.needsUpdate=!1}_=this.type,x.needsUpdate=!1,r.setRenderTarget(C,b,N)};function w(P,D){const F=e.update(M);m.defines.VSM_SAMPLES!==P.blurSamples&&(m.defines.VSM_SAMPLES=P.blurSamples,g.defines.VSM_SAMPLES=P.blurSamples,m.needsUpdate=!0,g.needsUpdate=!0),P.mapPass===null&&(P.mapPass=new Ci(i.x,i.y)),m.uniforms.shadow_pass.value=P.map.texture,m.uniforms.resolution.value=P.mapSize,m.uniforms.radius.value=P.radius,r.setRenderTarget(P.mapPass),r.clear(),r.renderBufferDirect(D,null,F,m,M,null),g.uniforms.shadow_pass.value=P.mapPass.texture,g.uniforms.resolution.value=P.mapSize,g.uniforms.radius.value=P.radius,r.setRenderTarget(P.map),r.clear(),r.renderBufferDirect(D,null,F,g,M,null)}function E(P,D,F,C){let b=null;const N=F.isPointLight===!0?P.customDistanceMaterial:P.customDepthMaterial;if(N!==void 0)b=N;else if(b=F.isPointLight===!0?u:c,r.localClippingEnabled&&D.clipShadows===!0&&Array.isArray(D.clippingPlanes)&&D.clippingPlanes.length!==0||D.displacementMap&&D.displacementScale!==0||D.alphaMap&&D.alphaTest>0||D.map&&D.alphaTest>0){const q=b.uuid,Y=D.uuid;let K=h[q];K===void 0&&(K={},h[q]=K);let le=K[Y];le===void 0&&(le=b.clone(),K[Y]=le,D.addEventListener("dispose",U)),b=le}if(b.visible=D.visible,b.wireframe=D.wireframe,C===wi?b.side=D.shadowSide!==null?D.shadowSide:D.side:b.side=D.shadowSide!==null?D.shadowSide:p[D.side],b.alphaMap=D.alphaMap,b.alphaTest=D.alphaTest,b.map=D.map,b.clipShadows=D.clipShadows,b.clippingPlanes=D.clippingPlanes,b.clipIntersection=D.clipIntersection,b.displacementMap=D.displacementMap,b.displacementScale=D.displacementScale,b.displacementBias=D.displacementBias,b.wireframeLinewidth=D.wireframeLinewidth,b.linewidth=D.linewidth,F.isPointLight===!0&&b.isMeshDistanceMaterial===!0){const q=r.properties.get(b);q.light=F}return b}function T(P,D,F,C,b){if(P.visible===!1)return;if(P.layers.test(D.layers)&&(P.isMesh||P.isLine||P.isPoints)&&(P.castShadow||P.receiveShadow&&b===wi)&&(!P.frustumCulled||n.intersectsObject(P))){P.modelViewMatrix.multiplyMatrices(F.matrixWorldInverse,P.matrixWorld);const Y=e.update(P),K=P.material;if(Array.isArray(K)){const le=Y.groups;for(let $=0,pe=le.length;$<pe;$++){const J=le[$],xe=K[J.materialIndex];if(xe&&xe.visible){const me=E(P,xe,C,b);P.onBeforeShadow(r,P,D,F,Y,me,J),r.renderBufferDirect(F,null,Y,me,P,J),P.onAfterShadow(r,P,D,F,Y,me,J)}}}else if(K.visible){const le=E(P,K,C,b);P.onBeforeShadow(r,P,D,F,Y,le,null),r.renderBufferDirect(F,null,Y,le,P,null),P.onAfterShadow(r,P,D,F,Y,le,null)}}const q=P.children;for(let Y=0,K=q.length;Y<K;Y++)T(q[Y],D,F,C,b)}function U(P){P.target.removeEventListener("dispose",U);for(const F in h){const C=h[F],b=P.target.uuid;b in C&&(C[b].dispose(),delete C[b])}}}const NT={[hu]:fu,[du]:gu,[pu]:vu,[Is]:mu,[fu]:hu,[gu]:du,[vu]:pu,[mu]:Is};function OT(r,e){function t(){let k=!1;const ye=new At;let te=null;const ue=new At(0,0,0,0);return{setMask:function(Ue){te!==Ue&&!k&&(r.colorMask(Ue,Ue,Ue,Ue),te=Ue)},setLocked:function(Ue){k=Ue},setClear:function(Ue,Ce,nt,It,Ht){Ht===!0&&(Ue*=It,Ce*=It,nt*=It),ye.set(Ue,Ce,nt,It),ue.equals(ye)===!1&&(r.clearColor(Ue,Ce,nt,It),ue.copy(ye))},reset:function(){k=!1,te=null,ue.set(-1,0,0,0)}}}function n(){let k=!1,ye=!1,te=null,ue=null,Ue=null;return{setReversed:function(Ce){if(ye!==Ce){const nt=e.get("EXT_clip_control");ye?nt.clipControlEXT(nt.LOWER_LEFT_EXT,nt.ZERO_TO_ONE_EXT):nt.clipControlEXT(nt.LOWER_LEFT_EXT,nt.NEGATIVE_ONE_TO_ONE_EXT);const It=Ue;Ue=null,this.setClear(It)}ye=Ce},getReversed:function(){return ye},setTest:function(Ce){Ce?we(r.DEPTH_TEST):et(r.DEPTH_TEST)},setMask:function(Ce){te!==Ce&&!k&&(r.depthMask(Ce),te=Ce)},setFunc:function(Ce){if(ye&&(Ce=NT[Ce]),ue!==Ce){switch(Ce){case hu:r.depthFunc(r.NEVER);break;case fu:r.depthFunc(r.ALWAYS);break;case du:r.depthFunc(r.LESS);break;case Is:r.depthFunc(r.LEQUAL);break;case pu:r.depthFunc(r.EQUAL);break;case mu:r.depthFunc(r.GEQUAL);break;case gu:r.depthFunc(r.GREATER);break;case vu:r.depthFunc(r.NOTEQUAL);break;default:r.depthFunc(r.LEQUAL)}ue=Ce}},setLocked:function(Ce){k=Ce},setClear:function(Ce){Ue!==Ce&&(ye&&(Ce=1-Ce),r.clearDepth(Ce),Ue=Ce)},reset:function(){k=!1,te=null,ue=null,Ue=null,ye=!1}}}function i(){let k=!1,ye=null,te=null,ue=null,Ue=null,Ce=null,nt=null,It=null,Ht=null;return{setTest:function(bt){k||(bt?we(r.STENCIL_TEST):et(r.STENCIL_TEST))},setMask:function(bt){ye!==bt&&!k&&(r.stencilMask(bt),ye=bt)},setFunc:function(bt,rn,Tn){(te!==bt||ue!==rn||Ue!==Tn)&&(r.stencilFunc(bt,rn,Tn),te=bt,ue=rn,Ue=Tn)},setOp:function(bt,rn,Tn){(Ce!==bt||nt!==rn||It!==Tn)&&(r.stencilOp(bt,rn,Tn),Ce=bt,nt=rn,It=Tn)},setLocked:function(bt){k=bt},setClear:function(bt){Ht!==bt&&(r.clearStencil(bt),Ht=bt)},reset:function(){k=!1,ye=null,te=null,ue=null,Ue=null,Ce=null,nt=null,It=null,Ht=null}}}const s=new t,l=new n,c=new i,u=new WeakMap,h=new WeakMap;let f={},p={},m=new WeakMap,g=[],y=null,M=!1,x=null,_=null,w=null,E=null,T=null,U=null,P=null,D=new Be(0,0,0),F=0,C=!1,b=null,N=null,q=null,Y=null,K=null;const le=r.getParameter(r.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let $=!1,pe=0;const J=r.getParameter(r.VERSION);J.indexOf("WebGL")!==-1?(pe=parseFloat(/^WebGL (\d)/.exec(J)[1]),$=pe>=1):J.indexOf("OpenGL ES")!==-1&&(pe=parseFloat(/^OpenGL ES (\d)/.exec(J)[1]),$=pe>=2);let xe=null,me={};const Se=r.getParameter(r.SCISSOR_BOX),Qe=r.getParameter(r.VIEWPORT),Je=new At().fromArray(Se),se=new At().fromArray(Qe);function ge(k,ye,te,ue){const Ue=new Uint8Array(4),Ce=r.createTexture();r.bindTexture(k,Ce),r.texParameteri(k,r.TEXTURE_MIN_FILTER,r.NEAREST),r.texParameteri(k,r.TEXTURE_MAG_FILTER,r.NEAREST);for(let nt=0;nt<te;nt++)k===r.TEXTURE_3D||k===r.TEXTURE_2D_ARRAY?r.texImage3D(ye,0,r.RGBA,1,1,ue,0,r.RGBA,r.UNSIGNED_BYTE,Ue):r.texImage2D(ye+nt,0,r.RGBA,1,1,0,r.RGBA,r.UNSIGNED_BYTE,Ue);return Ce}const Ve={};Ve[r.TEXTURE_2D]=ge(r.TEXTURE_2D,r.TEXTURE_2D,1),Ve[r.TEXTURE_CUBE_MAP]=ge(r.TEXTURE_CUBE_MAP,r.TEXTURE_CUBE_MAP_POSITIVE_X,6),Ve[r.TEXTURE_2D_ARRAY]=ge(r.TEXTURE_2D_ARRAY,r.TEXTURE_2D_ARRAY,1,1),Ve[r.TEXTURE_3D]=ge(r.TEXTURE_3D,r.TEXTURE_3D,1,1),s.setClear(0,0,0,1),l.setClear(1),c.setClear(0),we(r.DEPTH_TEST),l.setFunc(Is),ve(!1),Oe(Od),we(r.CULL_FACE),z(mr);function we(k){f[k]!==!0&&(r.enable(k),f[k]=!0)}function et(k){f[k]!==!1&&(r.disable(k),f[k]=!1)}function lt(k,ye){return p[k]!==ye?(r.bindFramebuffer(k,ye),p[k]=ye,k===r.DRAW_FRAMEBUFFER&&(p[r.FRAMEBUFFER]=ye),k===r.FRAMEBUFFER&&(p[r.DRAW_FRAMEBUFFER]=ye),!0):!1}function tt(k,ye){let te=g,ue=!1;if(k){te=m.get(ye),te===void 0&&(te=[],m.set(ye,te));const Ue=k.textures;if(te.length!==Ue.length||te[0]!==r.COLOR_ATTACHMENT0){for(let Ce=0,nt=Ue.length;Ce<nt;Ce++)te[Ce]=r.COLOR_ATTACHMENT0+Ce;te.length=Ue.length,ue=!0}}else te[0]!==r.BACK&&(te[0]=r.BACK,ue=!0);ue&&r.drawBuffers(te)}function ft(k){return y!==k?(r.useProgram(k),y=k,!0):!1}const he={[zr]:r.FUNC_ADD,[Dv]:r.FUNC_SUBTRACT,[Uv]:r.FUNC_REVERSE_SUBTRACT};he[Nv]=r.MIN,he[Ov]=r.MAX;const de={[Fv]:r.ZERO,[Bv]:r.ONE,[zv]:r.SRC_COLOR,[cu]:r.SRC_ALPHA,[Xv]:r.SRC_ALPHA_SATURATE,[Gv]:r.DST_COLOR,[Hv]:r.DST_ALPHA,[kv]:r.ONE_MINUS_SRC_COLOR,[uu]:r.ONE_MINUS_SRC_ALPHA,[Wv]:r.ONE_MINUS_DST_COLOR,[Vv]:r.ONE_MINUS_DST_ALPHA,[Yv]:r.CONSTANT_COLOR,[qv]:r.ONE_MINUS_CONSTANT_COLOR,[Zv]:r.CONSTANT_ALPHA,[jv]:r.ONE_MINUS_CONSTANT_ALPHA};function z(k,ye,te,ue,Ue,Ce,nt,It,Ht,bt){if(k===mr){M===!0&&(et(r.BLEND),M=!1);return}if(M===!1&&(we(r.BLEND),M=!0),k!==Lv){if(k!==x||bt!==C){if((_!==zr||T!==zr)&&(r.blendEquation(r.FUNC_ADD),_=zr,T=zr),bt)switch(k){case Ts:r.blendFuncSeparate(r.ONE,r.ONE_MINUS_SRC_ALPHA,r.ONE,r.ONE_MINUS_SRC_ALPHA);break;case Fd:r.blendFunc(r.ONE,r.ONE);break;case Bd:r.blendFuncSeparate(r.ZERO,r.ONE_MINUS_SRC_COLOR,r.ZERO,r.ONE);break;case zd:r.blendFuncSeparate(r.ZERO,r.SRC_COLOR,r.ZERO,r.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",k);break}else switch(k){case Ts:r.blendFuncSeparate(r.SRC_ALPHA,r.ONE_MINUS_SRC_ALPHA,r.ONE,r.ONE_MINUS_SRC_ALPHA);break;case Fd:r.blendFunc(r.SRC_ALPHA,r.ONE);break;case Bd:r.blendFuncSeparate(r.ZERO,r.ONE_MINUS_SRC_COLOR,r.ZERO,r.ONE);break;case zd:r.blendFunc(r.ZERO,r.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",k);break}w=null,E=null,U=null,P=null,D.set(0,0,0),F=0,x=k,C=bt}return}Ue=Ue||ye,Ce=Ce||te,nt=nt||ue,(ye!==_||Ue!==T)&&(r.blendEquationSeparate(he[ye],he[Ue]),_=ye,T=Ue),(te!==w||ue!==E||Ce!==U||nt!==P)&&(r.blendFuncSeparate(de[te],de[ue],de[Ce],de[nt]),w=te,E=ue,U=Ce,P=nt),(It.equals(D)===!1||Ht!==F)&&(r.blendColor(It.r,It.g,It.b,Ht),D.copy(It),F=Ht),x=k,C=!1}function je(k,ye){k.side===Gi?et(r.CULL_FACE):we(r.CULL_FACE);let te=k.side===Vn;ye&&(te=!te),ve(te),k.blending===Ts&&k.transparent===!1?z(mr):z(k.blending,k.blendEquation,k.blendSrc,k.blendDst,k.blendEquationAlpha,k.blendSrcAlpha,k.blendDstAlpha,k.blendColor,k.blendAlpha,k.premultipliedAlpha),l.setFunc(k.depthFunc),l.setTest(k.depthTest),l.setMask(k.depthWrite),s.setMask(k.colorWrite);const ue=k.stencilWrite;c.setTest(ue),ue&&(c.setMask(k.stencilWriteMask),c.setFunc(k.stencilFunc,k.stencilRef,k.stencilFuncMask),c.setOp(k.stencilFail,k.stencilZFail,k.stencilZPass)),it(k.polygonOffset,k.polygonOffsetFactor,k.polygonOffsetUnits),k.alphaToCoverage===!0?we(r.SAMPLE_ALPHA_TO_COVERAGE):et(r.SAMPLE_ALPHA_TO_COVERAGE)}function ve(k){b!==k&&(k?r.frontFace(r.CW):r.frontFace(r.CCW),b=k)}function Oe(k){k!==Rv?(we(r.CULL_FACE),k!==N&&(k===Od?r.cullFace(r.BACK):k===Pv?r.cullFace(r.FRONT):r.cullFace(r.FRONT_AND_BACK))):et(r.CULL_FACE),N=k}function Te(k){k!==q&&($&&r.lineWidth(k),q=k)}function it(k,ye,te){k?(we(r.POLYGON_OFFSET_FILL),(Y!==ye||K!==te)&&(r.polygonOffset(ye,te),Y=ye,K=te)):et(r.POLYGON_OFFSET_FILL)}function Pe(k){k?we(r.SCISSOR_TEST):et(r.SCISSOR_TEST)}function O(k){k===void 0&&(k=r.TEXTURE0+le-1),xe!==k&&(r.activeTexture(k),xe=k)}function R(k,ye,te){te===void 0&&(xe===null?te=r.TEXTURE0+le-1:te=xe);let ue=me[te];ue===void 0&&(ue={type:void 0,texture:void 0},me[te]=ue),(ue.type!==k||ue.texture!==ye)&&(xe!==te&&(r.activeTexture(te),xe=te),r.bindTexture(k,ye||Ve[k]),ue.type=k,ue.texture=ye)}function Z(){const k=me[xe];k!==void 0&&k.type!==void 0&&(r.bindTexture(k.type,null),k.type=void 0,k.texture=void 0)}function re(){try{r.compressedTexImage2D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function fe(){try{r.compressedTexImage3D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function ce(){try{r.texSubImage2D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function We(){try{r.texSubImage3D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function Ae(){try{r.compressedTexSubImage2D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function Fe(){try{r.compressedTexSubImage3D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function St(){try{r.texStorage2D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function _e(){try{r.texStorage3D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function He(){try{r.texImage2D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function rt(){try{r.texImage3D.apply(r,arguments)}catch(k){console.error("THREE.WebGLState:",k)}}function ct(k){Je.equals(k)===!1&&(r.scissor(k.x,k.y,k.z,k.w),Je.copy(k))}function ze(k){se.equals(k)===!1&&(r.viewport(k.x,k.y,k.z,k.w),se.copy(k))}function H(k,ye){let te=h.get(ye);te===void 0&&(te=new WeakMap,h.set(ye,te));let ue=te.get(k);ue===void 0&&(ue=r.getUniformBlockIndex(ye,k.name),te.set(k,ue))}function oe(k,ye){const ue=h.get(ye).get(k);u.get(ye)!==ue&&(r.uniformBlockBinding(ye,ue,k.__bindingPointIndex),u.set(ye,ue))}function Re(){r.disable(r.BLEND),r.disable(r.CULL_FACE),r.disable(r.DEPTH_TEST),r.disable(r.POLYGON_OFFSET_FILL),r.disable(r.SCISSOR_TEST),r.disable(r.STENCIL_TEST),r.disable(r.SAMPLE_ALPHA_TO_COVERAGE),r.blendEquation(r.FUNC_ADD),r.blendFunc(r.ONE,r.ZERO),r.blendFuncSeparate(r.ONE,r.ZERO,r.ONE,r.ZERO),r.blendColor(0,0,0,0),r.colorMask(!0,!0,!0,!0),r.clearColor(0,0,0,0),r.depthMask(!0),r.depthFunc(r.LESS),l.setReversed(!1),r.clearDepth(1),r.stencilMask(4294967295),r.stencilFunc(r.ALWAYS,0,4294967295),r.stencilOp(r.KEEP,r.KEEP,r.KEEP),r.clearStencil(0),r.cullFace(r.BACK),r.frontFace(r.CCW),r.polygonOffset(0,0),r.activeTexture(r.TEXTURE0),r.bindFramebuffer(r.FRAMEBUFFER,null),r.bindFramebuffer(r.DRAW_FRAMEBUFFER,null),r.bindFramebuffer(r.READ_FRAMEBUFFER,null),r.useProgram(null),r.lineWidth(1),r.scissor(0,0,r.canvas.width,r.canvas.height),r.viewport(0,0,r.canvas.width,r.canvas.height),f={},xe=null,me={},p={},m=new WeakMap,g=[],y=null,M=!1,x=null,_=null,w=null,E=null,T=null,U=null,P=null,D=new Be(0,0,0),F=0,C=!1,b=null,N=null,q=null,Y=null,K=null,Je.set(0,0,r.canvas.width,r.canvas.height),se.set(0,0,r.canvas.width,r.canvas.height),s.reset(),l.reset(),c.reset()}return{buffers:{color:s,depth:l,stencil:c},enable:we,disable:et,bindFramebuffer:lt,drawBuffers:tt,useProgram:ft,setBlending:z,setMaterial:je,setFlipSided:ve,setCullFace:Oe,setLineWidth:Te,setPolygonOffset:it,setScissorTest:Pe,activeTexture:O,bindTexture:R,unbindTexture:Z,compressedTexImage2D:re,compressedTexImage3D:fe,texImage2D:He,texImage3D:rt,updateUBOMapping:H,uniformBlockBinding:oe,texStorage2D:St,texStorage3D:_e,texSubImage2D:ce,texSubImage3D:We,compressedTexSubImage2D:Ae,compressedTexSubImage3D:Fe,scissor:ct,viewport:ze,reset:Re}}function FT(r,e){const t=r.image&&r.image.width?r.image.width/r.image.height:1;return t>e?(r.repeat.x=1,r.repeat.y=t/e,r.offset.x=0,r.offset.y=(1-r.repeat.y)/2):(r.repeat.x=e/t,r.repeat.y=1,r.offset.x=(1-r.repeat.x)/2,r.offset.y=0),r}function BT(r,e){const t=r.image&&r.image.width?r.image.width/r.image.height:1;return t>e?(r.repeat.x=e/t,r.repeat.y=1,r.offset.x=(1-r.repeat.x)/2,r.offset.y=0):(r.repeat.x=1,r.repeat.y=t/e,r.offset.x=0,r.offset.y=(1-r.repeat.y)/2),r}function zT(r){return r.repeat.x=1,r.repeat.y=1,r.offset.x=0,r.offset.y=0,r}function Xd(r,e,t,n){const i=kT(n);switch(t){case op:return r*e;case lp:return r*e;case cp:return r*e*2;case nh:return r*e/i.components*i.byteLength;case Qa:return r*e/i.components*i.byteLength;case up:return r*e*2/i.components*i.byteLength;case ih:return r*e*2/i.components*i.byteLength;case ap:return r*e*3/i.components*i.byteLength;case Dn:return r*e*4/i.components*i.byteLength;case rh:return r*e*4/i.components*i.byteLength;case Ta:case Aa:return Math.floor((r+3)/4)*Math.floor((e+3)/4)*8;case ba:case Ca:return Math.floor((r+3)/4)*Math.floor((e+3)/4)*16;case yu:case Su:return Math.max(r,16)*Math.max(e,8)/4;case _u:case xu:return Math.max(r,8)*Math.max(e,8)/2;case Mu:case Eu:return Math.floor((r+3)/4)*Math.floor((e+3)/4)*8;case wu:return Math.floor((r+3)/4)*Math.floor((e+3)/4)*16;case Tu:return Math.floor((r+3)/4)*Math.floor((e+3)/4)*16;case Au:return Math.floor((r+4)/5)*Math.floor((e+3)/4)*16;case bu:return Math.floor((r+4)/5)*Math.floor((e+4)/5)*16;case Cu:return Math.floor((r+5)/6)*Math.floor((e+4)/5)*16;case Ru:return Math.floor((r+5)/6)*Math.floor((e+5)/6)*16;case Pu:return Math.floor((r+7)/8)*Math.floor((e+4)/5)*16;case Iu:return Math.floor((r+7)/8)*Math.floor((e+5)/6)*16;case Lu:return Math.floor((r+7)/8)*Math.floor((e+7)/8)*16;case Du:return Math.floor((r+9)/10)*Math.floor((e+4)/5)*16;case Uu:return Math.floor((r+9)/10)*Math.floor((e+5)/6)*16;case Nu:return Math.floor((r+9)/10)*Math.floor((e+7)/8)*16;case Ou:return Math.floor((r+9)/10)*Math.floor((e+9)/10)*16;case Fu:return Math.floor((r+11)/12)*Math.floor((e+9)/10)*16;case Bu:return Math.floor((r+11)/12)*Math.floor((e+11)/12)*16;case Ra:case zu:case ku:return Math.ceil(r/4)*Math.ceil(e/4)*16;case hp:case Hu:return Math.ceil(r/4)*Math.ceil(e/4)*8;case Vu:case Gu:return Math.ceil(r/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function kT(r){switch(r){case bi:case ip:return{byteLength:1,components:1};case Io:case rp:case Fo:return{byteLength:2,components:1};case eh:case th:return{byteLength:2,components:4};case yr:case $u:case Kn:return{byteLength:4,components:1};case sp:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${r}.`)}const HT={contain:FT,cover:BT,fill:zT,getByteLength:Xd};function VT(r,e,t,n,i,s,l){const c=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,u=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),h=new ae,f=new WeakMap;let p;const m=new WeakMap;let g=!1;try{g=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function y(O,R){return g?new OffscreenCanvas(O,R):Ha("canvas")}function M(O,R,Z){let re=1;const fe=Pe(O);if((fe.width>Z||fe.height>Z)&&(re=Z/Math.max(fe.width,fe.height)),re<1)if(typeof HTMLImageElement<"u"&&O instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&O instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&O instanceof ImageBitmap||typeof VideoFrame<"u"&&O instanceof VideoFrame){const ce=Math.floor(re*fe.width),We=Math.floor(re*fe.height);p===void 0&&(p=y(ce,We));const Ae=R?y(ce,We):p;return Ae.width=ce,Ae.height=We,Ae.getContext("2d").drawImage(O,0,0,ce,We),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+fe.width+"x"+fe.height+") to ("+ce+"x"+We+")."),Ae}else return"data"in O&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+fe.width+"x"+fe.height+")."),O;return O}function x(O){return O.generateMipmaps}function _(O){r.generateMipmap(O)}function w(O){return O.isWebGLCubeRenderTarget?r.TEXTURE_CUBE_MAP:O.isWebGL3DRenderTarget?r.TEXTURE_3D:O.isWebGLArrayRenderTarget||O.isCompressedArrayTexture?r.TEXTURE_2D_ARRAY:r.TEXTURE_2D}function E(O,R,Z,re,fe=!1){if(O!==null){if(r[O]!==void 0)return r[O];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+O+"'")}let ce=R;if(R===r.RED&&(Z===r.FLOAT&&(ce=r.R32F),Z===r.HALF_FLOAT&&(ce=r.R16F),Z===r.UNSIGNED_BYTE&&(ce=r.R8)),R===r.RED_INTEGER&&(Z===r.UNSIGNED_BYTE&&(ce=r.R8UI),Z===r.UNSIGNED_SHORT&&(ce=r.R16UI),Z===r.UNSIGNED_INT&&(ce=r.R32UI),Z===r.BYTE&&(ce=r.R8I),Z===r.SHORT&&(ce=r.R16I),Z===r.INT&&(ce=r.R32I)),R===r.RG&&(Z===r.FLOAT&&(ce=r.RG32F),Z===r.HALF_FLOAT&&(ce=r.RG16F),Z===r.UNSIGNED_BYTE&&(ce=r.RG8)),R===r.RG_INTEGER&&(Z===r.UNSIGNED_BYTE&&(ce=r.RG8UI),Z===r.UNSIGNED_SHORT&&(ce=r.RG16UI),Z===r.UNSIGNED_INT&&(ce=r.RG32UI),Z===r.BYTE&&(ce=r.RG8I),Z===r.SHORT&&(ce=r.RG16I),Z===r.INT&&(ce=r.RG32I)),R===r.RGB_INTEGER&&(Z===r.UNSIGNED_BYTE&&(ce=r.RGB8UI),Z===r.UNSIGNED_SHORT&&(ce=r.RGB16UI),Z===r.UNSIGNED_INT&&(ce=r.RGB32UI),Z===r.BYTE&&(ce=r.RGB8I),Z===r.SHORT&&(ce=r.RGB16I),Z===r.INT&&(ce=r.RGB32I)),R===r.RGBA_INTEGER&&(Z===r.UNSIGNED_BYTE&&(ce=r.RGBA8UI),Z===r.UNSIGNED_SHORT&&(ce=r.RGBA16UI),Z===r.UNSIGNED_INT&&(ce=r.RGBA32UI),Z===r.BYTE&&(ce=r.RGBA8I),Z===r.SHORT&&(ce=r.RGBA16I),Z===r.INT&&(ce=r.RGBA32I)),R===r.RGB&&Z===r.UNSIGNED_INT_5_9_9_9_REV&&(ce=r.RGB9_E5),R===r.RGBA){const We=fe?$a:Pt.getTransfer(re);Z===r.FLOAT&&(ce=r.RGBA32F),Z===r.HALF_FLOAT&&(ce=r.RGBA16F),Z===r.UNSIGNED_BYTE&&(ce=We===Ft?r.SRGB8_ALPHA8:r.RGBA8),Z===r.UNSIGNED_SHORT_4_4_4_4&&(ce=r.RGBA4),Z===r.UNSIGNED_SHORT_5_5_5_1&&(ce=r.RGB5_A1)}return(ce===r.R16F||ce===r.R32F||ce===r.RG16F||ce===r.RG32F||ce===r.RGBA16F||ce===r.RGBA32F)&&e.get("EXT_color_buffer_float"),ce}function T(O,R){let Z;return O?R===null||R===yr||R===Ls?Z=r.DEPTH24_STENCIL8:R===Kn?Z=r.DEPTH32F_STENCIL8:R===Io&&(Z=r.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):R===null||R===yr||R===Ls?Z=r.DEPTH_COMPONENT24:R===Kn?Z=r.DEPTH_COMPONENT32F:R===Io&&(Z=r.DEPTH_COMPONENT16),Z}function U(O,R){return x(O)===!0||O.isFramebufferTexture&&O.minFilter!==wn&&O.minFilter!==cn?Math.log2(Math.max(R.width,R.height))+1:O.mipmaps!==void 0&&O.mipmaps.length>0?O.mipmaps.length:O.isCompressedTexture&&Array.isArray(O.image)?R.mipmaps.length:1}function P(O){const R=O.target;R.removeEventListener("dispose",P),F(R),R.isVideoTexture&&f.delete(R)}function D(O){const R=O.target;R.removeEventListener("dispose",D),b(R)}function F(O){const R=n.get(O);if(R.__webglInit===void 0)return;const Z=O.source,re=m.get(Z);if(re){const fe=re[R.__cacheKey];fe.usedTimes--,fe.usedTimes===0&&C(O),Object.keys(re).length===0&&m.delete(Z)}n.remove(O)}function C(O){const R=n.get(O);r.deleteTexture(R.__webglTexture);const Z=O.source,re=m.get(Z);delete re[R.__cacheKey],l.memory.textures--}function b(O){const R=n.get(O);if(O.depthTexture&&(O.depthTexture.dispose(),n.remove(O.depthTexture)),O.isWebGLCubeRenderTarget)for(let re=0;re<6;re++){if(Array.isArray(R.__webglFramebuffer[re]))for(let fe=0;fe<R.__webglFramebuffer[re].length;fe++)r.deleteFramebuffer(R.__webglFramebuffer[re][fe]);else r.deleteFramebuffer(R.__webglFramebuffer[re]);R.__webglDepthbuffer&&r.deleteRenderbuffer(R.__webglDepthbuffer[re])}else{if(Array.isArray(R.__webglFramebuffer))for(let re=0;re<R.__webglFramebuffer.length;re++)r.deleteFramebuffer(R.__webglFramebuffer[re]);else r.deleteFramebuffer(R.__webglFramebuffer);if(R.__webglDepthbuffer&&r.deleteRenderbuffer(R.__webglDepthbuffer),R.__webglMultisampledFramebuffer&&r.deleteFramebuffer(R.__webglMultisampledFramebuffer),R.__webglColorRenderbuffer)for(let re=0;re<R.__webglColorRenderbuffer.length;re++)R.__webglColorRenderbuffer[re]&&r.deleteRenderbuffer(R.__webglColorRenderbuffer[re]);R.__webglDepthRenderbuffer&&r.deleteRenderbuffer(R.__webglDepthRenderbuffer)}const Z=O.textures;for(let re=0,fe=Z.length;re<fe;re++){const ce=n.get(Z[re]);ce.__webglTexture&&(r.deleteTexture(ce.__webglTexture),l.memory.textures--),n.remove(Z[re])}n.remove(O)}let N=0;function q(){N=0}function Y(){const O=N;return O>=i.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+O+" texture units while this GPU supports only "+i.maxTextures),N+=1,O}function K(O){const R=[];return R.push(O.wrapS),R.push(O.wrapT),R.push(O.wrapR||0),R.push(O.magFilter),R.push(O.minFilter),R.push(O.anisotropy),R.push(O.internalFormat),R.push(O.format),R.push(O.type),R.push(O.generateMipmaps),R.push(O.premultiplyAlpha),R.push(O.flipY),R.push(O.unpackAlignment),R.push(O.colorSpace),R.join()}function le(O,R){const Z=n.get(O);if(O.isVideoTexture&&Te(O),O.isRenderTargetTexture===!1&&O.version>0&&Z.__version!==O.version){const re=O.image;if(re===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(re.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{se(Z,O,R);return}}t.bindTexture(r.TEXTURE_2D,Z.__webglTexture,r.TEXTURE0+R)}function $(O,R){const Z=n.get(O);if(O.version>0&&Z.__version!==O.version){se(Z,O,R);return}t.bindTexture(r.TEXTURE_2D_ARRAY,Z.__webglTexture,r.TEXTURE0+R)}function pe(O,R){const Z=n.get(O);if(O.version>0&&Z.__version!==O.version){se(Z,O,R);return}t.bindTexture(r.TEXTURE_3D,Z.__webglTexture,r.TEXTURE0+R)}function J(O,R){const Z=n.get(O);if(O.version>0&&Z.__version!==O.version){ge(Z,O,R);return}t.bindTexture(r.TEXTURE_CUBE_MAP,Z.__webglTexture,r.TEXTURE0+R)}const xe={[Na]:r.REPEAT,[vi]:r.CLAMP_TO_EDGE,[Oa]:r.MIRRORED_REPEAT},me={[wn]:r.NEAREST,[np]:r.NEAREST_MIPMAP_NEAREST,[wo]:r.NEAREST_MIPMAP_LINEAR,[cn]:r.LINEAR,[wa]:r.LINEAR_MIPMAP_NEAREST,[Xi]:r.LINEAR_MIPMAP_LINEAR},Se={[h_]:r.NEVER,[v_]:r.ALWAYS,[f_]:r.LESS,[dp]:r.LEQUAL,[d_]:r.EQUAL,[g_]:r.GEQUAL,[p_]:r.GREATER,[m_]:r.NOTEQUAL};function Qe(O,R){if(R.type===Kn&&e.has("OES_texture_float_linear")===!1&&(R.magFilter===cn||R.magFilter===wa||R.magFilter===wo||R.magFilter===Xi||R.minFilter===cn||R.minFilter===wa||R.minFilter===wo||R.minFilter===Xi)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),r.texParameteri(O,r.TEXTURE_WRAP_S,xe[R.wrapS]),r.texParameteri(O,r.TEXTURE_WRAP_T,xe[R.wrapT]),(O===r.TEXTURE_3D||O===r.TEXTURE_2D_ARRAY)&&r.texParameteri(O,r.TEXTURE_WRAP_R,xe[R.wrapR]),r.texParameteri(O,r.TEXTURE_MAG_FILTER,me[R.magFilter]),r.texParameteri(O,r.TEXTURE_MIN_FILTER,me[R.minFilter]),R.compareFunction&&(r.texParameteri(O,r.TEXTURE_COMPARE_MODE,r.COMPARE_REF_TO_TEXTURE),r.texParameteri(O,r.TEXTURE_COMPARE_FUNC,Se[R.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(R.magFilter===wn||R.minFilter!==wo&&R.minFilter!==Xi||R.type===Kn&&e.has("OES_texture_float_linear")===!1)return;if(R.anisotropy>1||n.get(R).__currentAnisotropy){const Z=e.get("EXT_texture_filter_anisotropic");r.texParameterf(O,Z.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(R.anisotropy,i.getMaxAnisotropy())),n.get(R).__currentAnisotropy=R.anisotropy}}}function Je(O,R){let Z=!1;O.__webglInit===void 0&&(O.__webglInit=!0,R.addEventListener("dispose",P));const re=R.source;let fe=m.get(re);fe===void 0&&(fe={},m.set(re,fe));const ce=K(R);if(ce!==O.__cacheKey){fe[ce]===void 0&&(fe[ce]={texture:r.createTexture(),usedTimes:0},l.memory.textures++,Z=!0),fe[ce].usedTimes++;const We=fe[O.__cacheKey];We!==void 0&&(fe[O.__cacheKey].usedTimes--,We.usedTimes===0&&C(R)),O.__cacheKey=ce,O.__webglTexture=fe[ce].texture}return Z}function se(O,R,Z){let re=r.TEXTURE_2D;(R.isDataArrayTexture||R.isCompressedArrayTexture)&&(re=r.TEXTURE_2D_ARRAY),R.isData3DTexture&&(re=r.TEXTURE_3D);const fe=Je(O,R),ce=R.source;t.bindTexture(re,O.__webglTexture,r.TEXTURE0+Z);const We=n.get(ce);if(ce.version!==We.__version||fe===!0){t.activeTexture(r.TEXTURE0+Z);const Ae=Pt.getPrimaries(Pt.workingColorSpace),Fe=R.colorSpace===fr?null:Pt.getPrimaries(R.colorSpace),St=R.colorSpace===fr||Ae===Fe?r.NONE:r.BROWSER_DEFAULT_WEBGL;r.pixelStorei(r.UNPACK_FLIP_Y_WEBGL,R.flipY),r.pixelStorei(r.UNPACK_PREMULTIPLY_ALPHA_WEBGL,R.premultiplyAlpha),r.pixelStorei(r.UNPACK_ALIGNMENT,R.unpackAlignment),r.pixelStorei(r.UNPACK_COLORSPACE_CONVERSION_WEBGL,St);let _e=M(R.image,!1,i.maxTextureSize);_e=it(R,_e);const He=s.convert(R.format,R.colorSpace),rt=s.convert(R.type);let ct=E(R.internalFormat,He,rt,R.colorSpace,R.isVideoTexture);Qe(re,R);let ze;const H=R.mipmaps,oe=R.isVideoTexture!==!0,Re=We.__version===void 0||fe===!0,k=ce.dataReady,ye=U(R,_e);if(R.isDepthTexture)ct=T(R.format===Ds,R.type),Re&&(oe?t.texStorage2D(r.TEXTURE_2D,1,ct,_e.width,_e.height):t.texImage2D(r.TEXTURE_2D,0,ct,_e.width,_e.height,0,He,rt,null));else if(R.isDataTexture)if(H.length>0){oe&&Re&&t.texStorage2D(r.TEXTURE_2D,ye,ct,H[0].width,H[0].height);for(let te=0,ue=H.length;te<ue;te++)ze=H[te],oe?k&&t.texSubImage2D(r.TEXTURE_2D,te,0,0,ze.width,ze.height,He,rt,ze.data):t.texImage2D(r.TEXTURE_2D,te,ct,ze.width,ze.height,0,He,rt,ze.data);R.generateMipmaps=!1}else oe?(Re&&t.texStorage2D(r.TEXTURE_2D,ye,ct,_e.width,_e.height),k&&t.texSubImage2D(r.TEXTURE_2D,0,0,0,_e.width,_e.height,He,rt,_e.data)):t.texImage2D(r.TEXTURE_2D,0,ct,_e.width,_e.height,0,He,rt,_e.data);else if(R.isCompressedTexture)if(R.isCompressedArrayTexture){oe&&Re&&t.texStorage3D(r.TEXTURE_2D_ARRAY,ye,ct,H[0].width,H[0].height,_e.depth);for(let te=0,ue=H.length;te<ue;te++)if(ze=H[te],R.format!==Dn)if(He!==null)if(oe){if(k)if(R.layerUpdates.size>0){const Ue=Xd(ze.width,ze.height,R.format,R.type);for(const Ce of R.layerUpdates){const nt=ze.data.subarray(Ce*Ue/ze.data.BYTES_PER_ELEMENT,(Ce+1)*Ue/ze.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(r.TEXTURE_2D_ARRAY,te,0,0,Ce,ze.width,ze.height,1,He,nt)}R.clearLayerUpdates()}else t.compressedTexSubImage3D(r.TEXTURE_2D_ARRAY,te,0,0,0,ze.width,ze.height,_e.depth,He,ze.data)}else t.compressedTexImage3D(r.TEXTURE_2D_ARRAY,te,ct,ze.width,ze.height,_e.depth,0,ze.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else oe?k&&t.texSubImage3D(r.TEXTURE_2D_ARRAY,te,0,0,0,ze.width,ze.height,_e.depth,He,rt,ze.data):t.texImage3D(r.TEXTURE_2D_ARRAY,te,ct,ze.width,ze.height,_e.depth,0,He,rt,ze.data)}else{oe&&Re&&t.texStorage2D(r.TEXTURE_2D,ye,ct,H[0].width,H[0].height);for(let te=0,ue=H.length;te<ue;te++)ze=H[te],R.format!==Dn?He!==null?oe?k&&t.compressedTexSubImage2D(r.TEXTURE_2D,te,0,0,ze.width,ze.height,He,ze.data):t.compressedTexImage2D(r.TEXTURE_2D,te,ct,ze.width,ze.height,0,ze.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):oe?k&&t.texSubImage2D(r.TEXTURE_2D,te,0,0,ze.width,ze.height,He,rt,ze.data):t.texImage2D(r.TEXTURE_2D,te,ct,ze.width,ze.height,0,He,rt,ze.data)}else if(R.isDataArrayTexture)if(oe){if(Re&&t.texStorage3D(r.TEXTURE_2D_ARRAY,ye,ct,_e.width,_e.height,_e.depth),k)if(R.layerUpdates.size>0){const te=Xd(_e.width,_e.height,R.format,R.type);for(const ue of R.layerUpdates){const Ue=_e.data.subarray(ue*te/_e.data.BYTES_PER_ELEMENT,(ue+1)*te/_e.data.BYTES_PER_ELEMENT);t.texSubImage3D(r.TEXTURE_2D_ARRAY,0,0,0,ue,_e.width,_e.height,1,He,rt,Ue)}R.clearLayerUpdates()}else t.texSubImage3D(r.TEXTURE_2D_ARRAY,0,0,0,0,_e.width,_e.height,_e.depth,He,rt,_e.data)}else t.texImage3D(r.TEXTURE_2D_ARRAY,0,ct,_e.width,_e.height,_e.depth,0,He,rt,_e.data);else if(R.isData3DTexture)oe?(Re&&t.texStorage3D(r.TEXTURE_3D,ye,ct,_e.width,_e.height,_e.depth),k&&t.texSubImage3D(r.TEXTURE_3D,0,0,0,0,_e.width,_e.height,_e.depth,He,rt,_e.data)):t.texImage3D(r.TEXTURE_3D,0,ct,_e.width,_e.height,_e.depth,0,He,rt,_e.data);else if(R.isFramebufferTexture){if(Re)if(oe)t.texStorage2D(r.TEXTURE_2D,ye,ct,_e.width,_e.height);else{let te=_e.width,ue=_e.height;for(let Ue=0;Ue<ye;Ue++)t.texImage2D(r.TEXTURE_2D,Ue,ct,te,ue,0,He,rt,null),te>>=1,ue>>=1}}else if(H.length>0){if(oe&&Re){const te=Pe(H[0]);t.texStorage2D(r.TEXTURE_2D,ye,ct,te.width,te.height)}for(let te=0,ue=H.length;te<ue;te++)ze=H[te],oe?k&&t.texSubImage2D(r.TEXTURE_2D,te,0,0,He,rt,ze):t.texImage2D(r.TEXTURE_2D,te,ct,He,rt,ze);R.generateMipmaps=!1}else if(oe){if(Re){const te=Pe(_e);t.texStorage2D(r.TEXTURE_2D,ye,ct,te.width,te.height)}k&&t.texSubImage2D(r.TEXTURE_2D,0,0,0,He,rt,_e)}else t.texImage2D(r.TEXTURE_2D,0,ct,He,rt,_e);x(R)&&_(re),We.__version=ce.version,R.onUpdate&&R.onUpdate(R)}O.__version=R.version}function ge(O,R,Z){if(R.image.length!==6)return;const re=Je(O,R),fe=R.source;t.bindTexture(r.TEXTURE_CUBE_MAP,O.__webglTexture,r.TEXTURE0+Z);const ce=n.get(fe);if(fe.version!==ce.__version||re===!0){t.activeTexture(r.TEXTURE0+Z);const We=Pt.getPrimaries(Pt.workingColorSpace),Ae=R.colorSpace===fr?null:Pt.getPrimaries(R.colorSpace),Fe=R.colorSpace===fr||We===Ae?r.NONE:r.BROWSER_DEFAULT_WEBGL;r.pixelStorei(r.UNPACK_FLIP_Y_WEBGL,R.flipY),r.pixelStorei(r.UNPACK_PREMULTIPLY_ALPHA_WEBGL,R.premultiplyAlpha),r.pixelStorei(r.UNPACK_ALIGNMENT,R.unpackAlignment),r.pixelStorei(r.UNPACK_COLORSPACE_CONVERSION_WEBGL,Fe);const St=R.isCompressedTexture||R.image[0].isCompressedTexture,_e=R.image[0]&&R.image[0].isDataTexture,He=[];for(let ue=0;ue<6;ue++)!St&&!_e?He[ue]=M(R.image[ue],!0,i.maxCubemapSize):He[ue]=_e?R.image[ue].image:R.image[ue],He[ue]=it(R,He[ue]);const rt=He[0],ct=s.convert(R.format,R.colorSpace),ze=s.convert(R.type),H=E(R.internalFormat,ct,ze,R.colorSpace),oe=R.isVideoTexture!==!0,Re=ce.__version===void 0||re===!0,k=fe.dataReady;let ye=U(R,rt);Qe(r.TEXTURE_CUBE_MAP,R);let te;if(St){oe&&Re&&t.texStorage2D(r.TEXTURE_CUBE_MAP,ye,H,rt.width,rt.height);for(let ue=0;ue<6;ue++){te=He[ue].mipmaps;for(let Ue=0;Ue<te.length;Ue++){const Ce=te[Ue];R.format!==Dn?ct!==null?oe?k&&t.compressedTexSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue,0,0,Ce.width,Ce.height,ct,Ce.data):t.compressedTexImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue,H,Ce.width,Ce.height,0,Ce.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):oe?k&&t.texSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue,0,0,Ce.width,Ce.height,ct,ze,Ce.data):t.texImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue,H,Ce.width,Ce.height,0,ct,ze,Ce.data)}}}else{if(te=R.mipmaps,oe&&Re){te.length>0&&ye++;const ue=Pe(He[0]);t.texStorage2D(r.TEXTURE_CUBE_MAP,ye,H,ue.width,ue.height)}for(let ue=0;ue<6;ue++)if(_e){oe?k&&t.texSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,0,0,0,He[ue].width,He[ue].height,ct,ze,He[ue].data):t.texImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,0,H,He[ue].width,He[ue].height,0,ct,ze,He[ue].data);for(let Ue=0;Ue<te.length;Ue++){const nt=te[Ue].image[ue].image;oe?k&&t.texSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue+1,0,0,nt.width,nt.height,ct,ze,nt.data):t.texImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue+1,H,nt.width,nt.height,0,ct,ze,nt.data)}}else{oe?k&&t.texSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,0,0,0,ct,ze,He[ue]):t.texImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,0,H,ct,ze,He[ue]);for(let Ue=0;Ue<te.length;Ue++){const Ce=te[Ue];oe?k&&t.texSubImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue+1,0,0,ct,ze,Ce.image[ue]):t.texImage2D(r.TEXTURE_CUBE_MAP_POSITIVE_X+ue,Ue+1,H,ct,ze,Ce.image[ue])}}}x(R)&&_(r.TEXTURE_CUBE_MAP),ce.__version=fe.version,R.onUpdate&&R.onUpdate(R)}O.__version=R.version}function Ve(O,R,Z,re,fe,ce){const We=s.convert(Z.format,Z.colorSpace),Ae=s.convert(Z.type),Fe=E(Z.internalFormat,We,Ae,Z.colorSpace),St=n.get(R),_e=n.get(Z);if(_e.__renderTarget=R,!St.__hasExternalTextures){const He=Math.max(1,R.width>>ce),rt=Math.max(1,R.height>>ce);fe===r.TEXTURE_3D||fe===r.TEXTURE_2D_ARRAY?t.texImage3D(fe,ce,Fe,He,rt,R.depth,0,We,Ae,null):t.texImage2D(fe,ce,Fe,He,rt,0,We,Ae,null)}t.bindFramebuffer(r.FRAMEBUFFER,O),Oe(R)?c.framebufferTexture2DMultisampleEXT(r.FRAMEBUFFER,re,fe,_e.__webglTexture,0,ve(R)):(fe===r.TEXTURE_2D||fe>=r.TEXTURE_CUBE_MAP_POSITIVE_X&&fe<=r.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&r.framebufferTexture2D(r.FRAMEBUFFER,re,fe,_e.__webglTexture,ce),t.bindFramebuffer(r.FRAMEBUFFER,null)}function we(O,R,Z){if(r.bindRenderbuffer(r.RENDERBUFFER,O),R.depthBuffer){const re=R.depthTexture,fe=re&&re.isDepthTexture?re.type:null,ce=T(R.stencilBuffer,fe),We=R.stencilBuffer?r.DEPTH_STENCIL_ATTACHMENT:r.DEPTH_ATTACHMENT,Ae=ve(R);Oe(R)?c.renderbufferStorageMultisampleEXT(r.RENDERBUFFER,Ae,ce,R.width,R.height):Z?r.renderbufferStorageMultisample(r.RENDERBUFFER,Ae,ce,R.width,R.height):r.renderbufferStorage(r.RENDERBUFFER,ce,R.width,R.height),r.framebufferRenderbuffer(r.FRAMEBUFFER,We,r.RENDERBUFFER,O)}else{const re=R.textures;for(let fe=0;fe<re.length;fe++){const ce=re[fe],We=s.convert(ce.format,ce.colorSpace),Ae=s.convert(ce.type),Fe=E(ce.internalFormat,We,Ae,ce.colorSpace),St=ve(R);Z&&Oe(R)===!1?r.renderbufferStorageMultisample(r.RENDERBUFFER,St,Fe,R.width,R.height):Oe(R)?c.renderbufferStorageMultisampleEXT(r.RENDERBUFFER,St,Fe,R.width,R.height):r.renderbufferStorage(r.RENDERBUFFER,Fe,R.width,R.height)}}r.bindRenderbuffer(r.RENDERBUFFER,null)}function et(O,R){if(R&&R.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(r.FRAMEBUFFER,O),!(R.depthTexture&&R.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const re=n.get(R.depthTexture);re.__renderTarget=R,(!re.__webglTexture||R.depthTexture.image.width!==R.width||R.depthTexture.image.height!==R.height)&&(R.depthTexture.image.width=R.width,R.depthTexture.image.height=R.height,R.depthTexture.needsUpdate=!0),le(R.depthTexture,0);const fe=re.__webglTexture,ce=ve(R);if(R.depthTexture.format===As)Oe(R)?c.framebufferTexture2DMultisampleEXT(r.FRAMEBUFFER,r.DEPTH_ATTACHMENT,r.TEXTURE_2D,fe,0,ce):r.framebufferTexture2D(r.FRAMEBUFFER,r.DEPTH_ATTACHMENT,r.TEXTURE_2D,fe,0);else if(R.depthTexture.format===Ds)Oe(R)?c.framebufferTexture2DMultisampleEXT(r.FRAMEBUFFER,r.DEPTH_STENCIL_ATTACHMENT,r.TEXTURE_2D,fe,0,ce):r.framebufferTexture2D(r.FRAMEBUFFER,r.DEPTH_STENCIL_ATTACHMENT,r.TEXTURE_2D,fe,0);else throw new Error("Unknown depthTexture format")}function lt(O){const R=n.get(O),Z=O.isWebGLCubeRenderTarget===!0;if(R.__boundDepthTexture!==O.depthTexture){const re=O.depthTexture;if(R.__depthDisposeCallback&&R.__depthDisposeCallback(),re){const fe=()=>{delete R.__boundDepthTexture,delete R.__depthDisposeCallback,re.removeEventListener("dispose",fe)};re.addEventListener("dispose",fe),R.__depthDisposeCallback=fe}R.__boundDepthTexture=re}if(O.depthTexture&&!R.__autoAllocateDepthBuffer){if(Z)throw new Error("target.depthTexture not supported in Cube render targets");et(R.__webglFramebuffer,O)}else if(Z){R.__webglDepthbuffer=[];for(let re=0;re<6;re++)if(t.bindFramebuffer(r.FRAMEBUFFER,R.__webglFramebuffer[re]),R.__webglDepthbuffer[re]===void 0)R.__webglDepthbuffer[re]=r.createRenderbuffer(),we(R.__webglDepthbuffer[re],O,!1);else{const fe=O.stencilBuffer?r.DEPTH_STENCIL_ATTACHMENT:r.DEPTH_ATTACHMENT,ce=R.__webglDepthbuffer[re];r.bindRenderbuffer(r.RENDERBUFFER,ce),r.framebufferRenderbuffer(r.FRAMEBUFFER,fe,r.RENDERBUFFER,ce)}}else if(t.bindFramebuffer(r.FRAMEBUFFER,R.__webglFramebuffer),R.__webglDepthbuffer===void 0)R.__webglDepthbuffer=r.createRenderbuffer(),we(R.__webglDepthbuffer,O,!1);else{const re=O.stencilBuffer?r.DEPTH_STENCIL_ATTACHMENT:r.DEPTH_ATTACHMENT,fe=R.__webglDepthbuffer;r.bindRenderbuffer(r.RENDERBUFFER,fe),r.framebufferRenderbuffer(r.FRAMEBUFFER,re,r.RENDERBUFFER,fe)}t.bindFramebuffer(r.FRAMEBUFFER,null)}function tt(O,R,Z){const re=n.get(O);R!==void 0&&Ve(re.__webglFramebuffer,O,O.texture,r.COLOR_ATTACHMENT0,r.TEXTURE_2D,0),Z!==void 0&&lt(O)}function ft(O){const R=O.texture,Z=n.get(O),re=n.get(R);O.addEventListener("dispose",D);const fe=O.textures,ce=O.isWebGLCubeRenderTarget===!0,We=fe.length>1;if(We||(re.__webglTexture===void 0&&(re.__webglTexture=r.createTexture()),re.__version=R.version,l.memory.textures++),ce){Z.__webglFramebuffer=[];for(let Ae=0;Ae<6;Ae++)if(R.mipmaps&&R.mipmaps.length>0){Z.__webglFramebuffer[Ae]=[];for(let Fe=0;Fe<R.mipmaps.length;Fe++)Z.__webglFramebuffer[Ae][Fe]=r.createFramebuffer()}else Z.__webglFramebuffer[Ae]=r.createFramebuffer()}else{if(R.mipmaps&&R.mipmaps.length>0){Z.__webglFramebuffer=[];for(let Ae=0;Ae<R.mipmaps.length;Ae++)Z.__webglFramebuffer[Ae]=r.createFramebuffer()}else Z.__webglFramebuffer=r.createFramebuffer();if(We)for(let Ae=0,Fe=fe.length;Ae<Fe;Ae++){const St=n.get(fe[Ae]);St.__webglTexture===void 0&&(St.__webglTexture=r.createTexture(),l.memory.textures++)}if(O.samples>0&&Oe(O)===!1){Z.__webglMultisampledFramebuffer=r.createFramebuffer(),Z.__webglColorRenderbuffer=[],t.bindFramebuffer(r.FRAMEBUFFER,Z.__webglMultisampledFramebuffer);for(let Ae=0;Ae<fe.length;Ae++){const Fe=fe[Ae];Z.__webglColorRenderbuffer[Ae]=r.createRenderbuffer(),r.bindRenderbuffer(r.RENDERBUFFER,Z.__webglColorRenderbuffer[Ae]);const St=s.convert(Fe.format,Fe.colorSpace),_e=s.convert(Fe.type),He=E(Fe.internalFormat,St,_e,Fe.colorSpace,O.isXRRenderTarget===!0),rt=ve(O);r.renderbufferStorageMultisample(r.RENDERBUFFER,rt,He,O.width,O.height),r.framebufferRenderbuffer(r.FRAMEBUFFER,r.COLOR_ATTACHMENT0+Ae,r.RENDERBUFFER,Z.__webglColorRenderbuffer[Ae])}r.bindRenderbuffer(r.RENDERBUFFER,null),O.depthBuffer&&(Z.__webglDepthRenderbuffer=r.createRenderbuffer(),we(Z.__webglDepthRenderbuffer,O,!0)),t.bindFramebuffer(r.FRAMEBUFFER,null)}}if(ce){t.bindTexture(r.TEXTURE_CUBE_MAP,re.__webglTexture),Qe(r.TEXTURE_CUBE_MAP,R);for(let Ae=0;Ae<6;Ae++)if(R.mipmaps&&R.mipmaps.length>0)for(let Fe=0;Fe<R.mipmaps.length;Fe++)Ve(Z.__webglFramebuffer[Ae][Fe],O,R,r.COLOR_ATTACHMENT0,r.TEXTURE_CUBE_MAP_POSITIVE_X+Ae,Fe);else Ve(Z.__webglFramebuffer[Ae],O,R,r.COLOR_ATTACHMENT0,r.TEXTURE_CUBE_MAP_POSITIVE_X+Ae,0);x(R)&&_(r.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(We){for(let Ae=0,Fe=fe.length;Ae<Fe;Ae++){const St=fe[Ae],_e=n.get(St);t.bindTexture(r.TEXTURE_2D,_e.__webglTexture),Qe(r.TEXTURE_2D,St),Ve(Z.__webglFramebuffer,O,St,r.COLOR_ATTACHMENT0+Ae,r.TEXTURE_2D,0),x(St)&&_(r.TEXTURE_2D)}t.unbindTexture()}else{let Ae=r.TEXTURE_2D;if((O.isWebGL3DRenderTarget||O.isWebGLArrayRenderTarget)&&(Ae=O.isWebGL3DRenderTarget?r.TEXTURE_3D:r.TEXTURE_2D_ARRAY),t.bindTexture(Ae,re.__webglTexture),Qe(Ae,R),R.mipmaps&&R.mipmaps.length>0)for(let Fe=0;Fe<R.mipmaps.length;Fe++)Ve(Z.__webglFramebuffer[Fe],O,R,r.COLOR_ATTACHMENT0,Ae,Fe);else Ve(Z.__webglFramebuffer,O,R,r.COLOR_ATTACHMENT0,Ae,0);x(R)&&_(Ae),t.unbindTexture()}O.depthBuffer&&lt(O)}function he(O){const R=O.textures;for(let Z=0,re=R.length;Z<re;Z++){const fe=R[Z];if(x(fe)){const ce=w(O),We=n.get(fe).__webglTexture;t.bindTexture(ce,We),_(ce),t.unbindTexture()}}}const de=[],z=[];function je(O){if(O.samples>0){if(Oe(O)===!1){const R=O.textures,Z=O.width,re=O.height;let fe=r.COLOR_BUFFER_BIT;const ce=O.stencilBuffer?r.DEPTH_STENCIL_ATTACHMENT:r.DEPTH_ATTACHMENT,We=n.get(O),Ae=R.length>1;if(Ae)for(let Fe=0;Fe<R.length;Fe++)t.bindFramebuffer(r.FRAMEBUFFER,We.__webglMultisampledFramebuffer),r.framebufferRenderbuffer(r.FRAMEBUFFER,r.COLOR_ATTACHMENT0+Fe,r.RENDERBUFFER,null),t.bindFramebuffer(r.FRAMEBUFFER,We.__webglFramebuffer),r.framebufferTexture2D(r.DRAW_FRAMEBUFFER,r.COLOR_ATTACHMENT0+Fe,r.TEXTURE_2D,null,0);t.bindFramebuffer(r.READ_FRAMEBUFFER,We.__webglMultisampledFramebuffer),t.bindFramebuffer(r.DRAW_FRAMEBUFFER,We.__webglFramebuffer);for(let Fe=0;Fe<R.length;Fe++){if(O.resolveDepthBuffer&&(O.depthBuffer&&(fe|=r.DEPTH_BUFFER_BIT),O.stencilBuffer&&O.resolveStencilBuffer&&(fe|=r.STENCIL_BUFFER_BIT)),Ae){r.framebufferRenderbuffer(r.READ_FRAMEBUFFER,r.COLOR_ATTACHMENT0,r.RENDERBUFFER,We.__webglColorRenderbuffer[Fe]);const St=n.get(R[Fe]).__webglTexture;r.framebufferTexture2D(r.DRAW_FRAMEBUFFER,r.COLOR_ATTACHMENT0,r.TEXTURE_2D,St,0)}r.blitFramebuffer(0,0,Z,re,0,0,Z,re,fe,r.NEAREST),u===!0&&(de.length=0,z.length=0,de.push(r.COLOR_ATTACHMENT0+Fe),O.depthBuffer&&O.resolveDepthBuffer===!1&&(de.push(ce),z.push(ce),r.invalidateFramebuffer(r.DRAW_FRAMEBUFFER,z)),r.invalidateFramebuffer(r.READ_FRAMEBUFFER,de))}if(t.bindFramebuffer(r.READ_FRAMEBUFFER,null),t.bindFramebuffer(r.DRAW_FRAMEBUFFER,null),Ae)for(let Fe=0;Fe<R.length;Fe++){t.bindFramebuffer(r.FRAMEBUFFER,We.__webglMultisampledFramebuffer),r.framebufferRenderbuffer(r.FRAMEBUFFER,r.COLOR_ATTACHMENT0+Fe,r.RENDERBUFFER,We.__webglColorRenderbuffer[Fe]);const St=n.get(R[Fe]).__webglTexture;t.bindFramebuffer(r.FRAMEBUFFER,We.__webglFramebuffer),r.framebufferTexture2D(r.DRAW_FRAMEBUFFER,r.COLOR_ATTACHMENT0+Fe,r.TEXTURE_2D,St,0)}t.bindFramebuffer(r.DRAW_FRAMEBUFFER,We.__webglMultisampledFramebuffer)}else if(O.depthBuffer&&O.resolveDepthBuffer===!1&&u){const R=O.stencilBuffer?r.DEPTH_STENCIL_ATTACHMENT:r.DEPTH_ATTACHMENT;r.invalidateFramebuffer(r.DRAW_FRAMEBUFFER,[R])}}}function ve(O){return Math.min(i.maxSamples,O.samples)}function Oe(O){const R=n.get(O);return O.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&R.__useRenderToTexture!==!1}function Te(O){const R=l.render.frame;f.get(O)!==R&&(f.set(O,R),O.update())}function it(O,R){const Z=O.colorSpace,re=O.format,fe=O.type;return O.isCompressedTexture===!0||O.isVideoTexture===!0||Z!==Ns&&Z!==fr&&(Pt.getTransfer(Z)===Ft?(re!==Dn||fe!==bi)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",Z)),R}function Pe(O){return typeof HTMLImageElement<"u"&&O instanceof HTMLImageElement?(h.width=O.naturalWidth||O.width,h.height=O.naturalHeight||O.height):typeof VideoFrame<"u"&&O instanceof VideoFrame?(h.width=O.displayWidth,h.height=O.displayHeight):(h.width=O.width,h.height=O.height),h}this.allocateTextureUnit=Y,this.resetTextureUnits=q,this.setTexture2D=le,this.setTexture2DArray=$,this.setTexture3D=pe,this.setTextureCube=J,this.rebindTextures=tt,this.setupRenderTarget=ft,this.updateRenderTargetMipmap=he,this.updateMultisampleRenderTarget=je,this.setupDepthRenderbuffer=lt,this.setupFrameBufferTexture=Ve,this.useMultisampledRTT=Oe}function L_(r,e){function t(n,i=fr){let s;const l=Pt.getTransfer(i);if(n===bi)return r.UNSIGNED_BYTE;if(n===eh)return r.UNSIGNED_SHORT_4_4_4_4;if(n===th)return r.UNSIGNED_SHORT_5_5_5_1;if(n===sp)return r.UNSIGNED_INT_5_9_9_9_REV;if(n===ip)return r.BYTE;if(n===rp)return r.SHORT;if(n===Io)return r.UNSIGNED_SHORT;if(n===$u)return r.INT;if(n===yr)return r.UNSIGNED_INT;if(n===Kn)return r.FLOAT;if(n===Fo)return r.HALF_FLOAT;if(n===op)return r.ALPHA;if(n===ap)return r.RGB;if(n===Dn)return r.RGBA;if(n===lp)return r.LUMINANCE;if(n===cp)return r.LUMINANCE_ALPHA;if(n===As)return r.DEPTH_COMPONENT;if(n===Ds)return r.DEPTH_STENCIL;if(n===nh)return r.RED;if(n===Qa)return r.RED_INTEGER;if(n===up)return r.RG;if(n===ih)return r.RG_INTEGER;if(n===rh)return r.RGBA_INTEGER;if(n===Ta||n===Aa||n===ba||n===Ca)if(l===Ft)if(s=e.get("WEBGL_compressed_texture_s3tc_srgb"),s!==null){if(n===Ta)return s.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(n===Aa)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(n===ba)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(n===Ca)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(s=e.get("WEBGL_compressed_texture_s3tc"),s!==null){if(n===Ta)return s.COMPRESSED_RGB_S3TC_DXT1_EXT;if(n===Aa)return s.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(n===ba)return s.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(n===Ca)return s.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(n===_u||n===yu||n===xu||n===Su)if(s=e.get("WEBGL_compressed_texture_pvrtc"),s!==null){if(n===_u)return s.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(n===yu)return s.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(n===xu)return s.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(n===Su)return s.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(n===Mu||n===Eu||n===wu)if(s=e.get("WEBGL_compressed_texture_etc"),s!==null){if(n===Mu||n===Eu)return l===Ft?s.COMPRESSED_SRGB8_ETC2:s.COMPRESSED_RGB8_ETC2;if(n===wu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:s.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(n===Tu||n===Au||n===bu||n===Cu||n===Ru||n===Pu||n===Iu||n===Lu||n===Du||n===Uu||n===Nu||n===Ou||n===Fu||n===Bu)if(s=e.get("WEBGL_compressed_texture_astc"),s!==null){if(n===Tu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:s.COMPRESSED_RGBA_ASTC_4x4_KHR;if(n===Au)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:s.COMPRESSED_RGBA_ASTC_5x4_KHR;if(n===bu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:s.COMPRESSED_RGBA_ASTC_5x5_KHR;if(n===Cu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:s.COMPRESSED_RGBA_ASTC_6x5_KHR;if(n===Ru)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:s.COMPRESSED_RGBA_ASTC_6x6_KHR;if(n===Pu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:s.COMPRESSED_RGBA_ASTC_8x5_KHR;if(n===Iu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:s.COMPRESSED_RGBA_ASTC_8x6_KHR;if(n===Lu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:s.COMPRESSED_RGBA_ASTC_8x8_KHR;if(n===Du)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:s.COMPRESSED_RGBA_ASTC_10x5_KHR;if(n===Uu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:s.COMPRESSED_RGBA_ASTC_10x6_KHR;if(n===Nu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:s.COMPRESSED_RGBA_ASTC_10x8_KHR;if(n===Ou)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:s.COMPRESSED_RGBA_ASTC_10x10_KHR;if(n===Fu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:s.COMPRESSED_RGBA_ASTC_12x10_KHR;if(n===Bu)return l===Ft?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:s.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(n===Ra||n===zu||n===ku)if(s=e.get("EXT_texture_compression_bptc"),s!==null){if(n===Ra)return l===Ft?s.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:s.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(n===zu)return s.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(n===ku)return s.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(n===hp||n===Hu||n===Vu||n===Gu)if(s=e.get("EXT_texture_compression_rgtc"),s!==null){if(n===Ra)return s.COMPRESSED_RED_RGTC1_EXT;if(n===Hu)return s.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(n===Vu)return s.COMPRESSED_RED_GREEN_RGTC2_EXT;if(n===Gu)return s.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return n===Ls?r.UNSIGNED_INT_24_8:r[n]!==void 0?r[n]:null}return{convert:t}}class D_ extends tn{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e}}class bo extends Dt{constructor(){super(),this.isGroup=!0,this.type="Group"}}const GT={type:"move"};class ad{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new bo,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new bo,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new L,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new L),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new bo,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new L,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new L),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const n of e.hand.values())this._getHandJoint(t,n)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,n){let i=null,s=null,l=null;const c=this._targetRay,u=this._grip,h=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(h&&e.hand){l=!0;for(const M of e.hand.values()){const x=t.getJointPose(M,n),_=this._getHandJoint(h,M);x!==null&&(_.matrix.fromArray(x.transform.matrix),_.matrix.decompose(_.position,_.rotation,_.scale),_.matrixWorldNeedsUpdate=!0,_.jointRadius=x.radius),_.visible=x!==null}const f=h.joints["index-finger-tip"],p=h.joints["thumb-tip"],m=f.position.distanceTo(p.position),g=.02,y=.005;h.inputState.pinching&&m>g+y?(h.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!h.inputState.pinching&&m<=g-y&&(h.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else u!==null&&e.gripSpace&&(s=t.getPose(e.gripSpace,n),s!==null&&(u.matrix.fromArray(s.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,s.linearVelocity?(u.hasLinearVelocity=!0,u.linearVelocity.copy(s.linearVelocity)):u.hasLinearVelocity=!1,s.angularVelocity?(u.hasAngularVelocity=!0,u.angularVelocity.copy(s.angularVelocity)):u.hasAngularVelocity=!1));c!==null&&(i=t.getPose(e.targetRaySpace,n),i===null&&s!==null&&(i=s),i!==null&&(c.matrix.fromArray(i.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,i.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(i.linearVelocity)):c.hasLinearVelocity=!1,i.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(i.angularVelocity)):c.hasAngularVelocity=!1,this.dispatchEvent(GT)))}return c!==null&&(c.visible=i!==null),u!==null&&(u.visible=s!==null),h!==null&&(h.visible=l!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const n=new bo;n.matrixAutoUpdate=!1,n.visible=!1,e.joints[t.jointName]=n,e.add(n)}return e.joints[t.jointName]}}const WT=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,XT=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`;class YT{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,n){if(this.texture===null){const i=new Kt,s=e.properties.get(i);s.__webglTexture=t.texture,(t.depthNear!=n.depthNear||t.depthFar!=n.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=i}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,n=new _i({vertexShader:WT,fragmentShader:XT,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new nn(new Bo(20,20),n)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class qT extends Ji{constructor(e,t){super();const n=this;let i=null,s=1,l=null,c="local-floor",u=1,h=null,f=null,p=null,m=null,g=null,y=null;const M=new YT,x=t.getContextAttributes();let _=null,w=null;const E=[],T=[],U=new ae;let P=null;const D=new tn;D.viewport=new At;const F=new tn;F.viewport=new At;const C=[D,F],b=new D_;let N=null,q=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(se){let ge=E[se];return ge===void 0&&(ge=new ad,E[se]=ge),ge.getTargetRaySpace()},this.getControllerGrip=function(se){let ge=E[se];return ge===void 0&&(ge=new ad,E[se]=ge),ge.getGripSpace()},this.getHand=function(se){let ge=E[se];return ge===void 0&&(ge=new ad,E[se]=ge),ge.getHandSpace()};function Y(se){const ge=T.indexOf(se.inputSource);if(ge===-1)return;const Ve=E[ge];Ve!==void 0&&(Ve.update(se.inputSource,se.frame,h||l),Ve.dispatchEvent({type:se.type,data:se.inputSource}))}function K(){i.removeEventListener("select",Y),i.removeEventListener("selectstart",Y),i.removeEventListener("selectend",Y),i.removeEventListener("squeeze",Y),i.removeEventListener("squeezestart",Y),i.removeEventListener("squeezeend",Y),i.removeEventListener("end",K),i.removeEventListener("inputsourceschange",le);for(let se=0;se<E.length;se++){const ge=T[se];ge!==null&&(T[se]=null,E[se].disconnect(ge))}N=null,q=null,M.reset(),e.setRenderTarget(_),g=null,m=null,p=null,i=null,w=null,Je.stop(),n.isPresenting=!1,e.setPixelRatio(P),e.setSize(U.width,U.height,!1),n.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(se){s=se,n.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(se){c=se,n.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return h||l},this.setReferenceSpace=function(se){h=se},this.getBaseLayer=function(){return m!==null?m:g},this.getBinding=function(){return p},this.getFrame=function(){return y},this.getSession=function(){return i},this.setSession=async function(se){if(i=se,i!==null){if(_=e.getRenderTarget(),i.addEventListener("select",Y),i.addEventListener("selectstart",Y),i.addEventListener("selectend",Y),i.addEventListener("squeeze",Y),i.addEventListener("squeezestart",Y),i.addEventListener("squeezeend",Y),i.addEventListener("end",K),i.addEventListener("inputsourceschange",le),x.xrCompatible!==!0&&await t.makeXRCompatible(),P=e.getPixelRatio(),e.getSize(U),i.renderState.layers===void 0){const ge={antialias:x.antialias,alpha:!0,depth:x.depth,stencil:x.stencil,framebufferScaleFactor:s};g=new XRWebGLLayer(i,t,ge),i.updateRenderState({baseLayer:g}),e.setPixelRatio(1),e.setSize(g.framebufferWidth,g.framebufferHeight,!1),w=new Ci(g.framebufferWidth,g.framebufferHeight,{format:Dn,type:bi,colorSpace:e.outputColorSpace,stencilBuffer:x.stencil})}else{let ge=null,Ve=null,we=null;x.depth&&(we=x.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ge=x.stencil?Ds:As,Ve=x.stencil?Ls:yr);const et={colorFormat:t.RGBA8,depthFormat:we,scaleFactor:s};p=new XRWebGLBinding(i,t),m=p.createProjectionLayer(et),i.updateRenderState({layers:[m]}),e.setPixelRatio(1),e.setSize(m.textureWidth,m.textureHeight,!1),w=new Ci(m.textureWidth,m.textureHeight,{format:Dn,type:bi,depthTexture:new yp(m.textureWidth,m.textureHeight,Ve,void 0,void 0,void 0,void 0,void 0,void 0,ge),stencilBuffer:x.stencil,colorSpace:e.outputColorSpace,samples:x.antialias?4:0,resolveDepthBuffer:m.ignoreDepthValues===!1})}w.isXRRenderTarget=!0,this.setFoveation(u),h=null,l=await i.requestReferenceSpace(c),Je.setContext(i),Je.start(),n.isPresenting=!0,n.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(i!==null)return i.environmentBlendMode},this.getDepthTexture=function(){return M.getDepthTexture()};function le(se){for(let ge=0;ge<se.removed.length;ge++){const Ve=se.removed[ge],we=T.indexOf(Ve);we>=0&&(T[we]=null,E[we].disconnect(Ve))}for(let ge=0;ge<se.added.length;ge++){const Ve=se.added[ge];let we=T.indexOf(Ve);if(we===-1){for(let lt=0;lt<E.length;lt++)if(lt>=T.length){T.push(Ve),we=lt;break}else if(T[lt]===null){T[lt]=Ve,we=lt;break}if(we===-1)break}const et=E[we];et&&et.connect(Ve)}}const $=new L,pe=new L;function J(se,ge,Ve){$.setFromMatrixPosition(ge.matrixWorld),pe.setFromMatrixPosition(Ve.matrixWorld);const we=$.distanceTo(pe),et=ge.projectionMatrix.elements,lt=Ve.projectionMatrix.elements,tt=et[14]/(et[10]-1),ft=et[14]/(et[10]+1),he=(et[9]+1)/et[5],de=(et[9]-1)/et[5],z=(et[8]-1)/et[0],je=(lt[8]+1)/lt[0],ve=tt*z,Oe=tt*je,Te=we/(-z+je),it=Te*-z;if(ge.matrixWorld.decompose(se.position,se.quaternion,se.scale),se.translateX(it),se.translateZ(Te),se.matrixWorld.compose(se.position,se.quaternion,se.scale),se.matrixWorldInverse.copy(se.matrixWorld).invert(),et[10]===-1)se.projectionMatrix.copy(ge.projectionMatrix),se.projectionMatrixInverse.copy(ge.projectionMatrixInverse);else{const Pe=tt+Te,O=ft+Te,R=ve-it,Z=Oe+(we-it),re=he*ft/O*Pe,fe=de*ft/O*Pe;se.projectionMatrix.makePerspective(R,Z,re,fe,Pe,O),se.projectionMatrixInverse.copy(se.projectionMatrix).invert()}}function xe(se,ge){ge===null?se.matrixWorld.copy(se.matrix):se.matrixWorld.multiplyMatrices(ge.matrixWorld,se.matrix),se.matrixWorldInverse.copy(se.matrixWorld).invert()}this.updateCamera=function(se){if(i===null)return;let ge=se.near,Ve=se.far;M.texture!==null&&(M.depthNear>0&&(ge=M.depthNear),M.depthFar>0&&(Ve=M.depthFar)),b.near=F.near=D.near=ge,b.far=F.far=D.far=Ve,(N!==b.near||q!==b.far)&&(i.updateRenderState({depthNear:b.near,depthFar:b.far}),N=b.near,q=b.far),D.layers.mask=se.layers.mask|2,F.layers.mask=se.layers.mask|4,b.layers.mask=D.layers.mask|F.layers.mask;const we=se.parent,et=b.cameras;xe(b,we);for(let lt=0;lt<et.length;lt++)xe(et[lt],we);et.length===2?J(b,D,F):b.projectionMatrix.copy(D.projectionMatrix),me(se,b,we)};function me(se,ge,Ve){Ve===null?se.matrix.copy(ge.matrixWorld):(se.matrix.copy(Ve.matrixWorld),se.matrix.invert(),se.matrix.multiply(ge.matrixWorld)),se.matrix.decompose(se.position,se.quaternion,se.scale),se.updateMatrixWorld(!0),se.projectionMatrix.copy(ge.projectionMatrix),se.projectionMatrixInverse.copy(ge.projectionMatrixInverse),se.isPerspectiveCamera&&(se.fov=Lo*2*Math.atan(1/se.projectionMatrix.elements[5]),se.zoom=1)}this.getCamera=function(){return b},this.getFoveation=function(){if(!(m===null&&g===null))return u},this.setFoveation=function(se){u=se,m!==null&&(m.fixedFoveation=se),g!==null&&g.fixedFoveation!==void 0&&(g.fixedFoveation=se)},this.hasDepthSensing=function(){return M.texture!==null},this.getDepthSensingMesh=function(){return M.getMesh(b)};let Se=null;function Qe(se,ge){if(f=ge.getViewerPose(h||l),y=ge,f!==null){const Ve=f.views;g!==null&&(e.setRenderTargetFramebuffer(w,g.framebuffer),e.setRenderTarget(w));let we=!1;Ve.length!==b.cameras.length&&(b.cameras.length=0,we=!0);for(let lt=0;lt<Ve.length;lt++){const tt=Ve[lt];let ft=null;if(g!==null)ft=g.getViewport(tt);else{const de=p.getViewSubImage(m,tt);ft=de.viewport,lt===0&&(e.setRenderTargetTextures(w,de.colorTexture,m.ignoreDepthValues?void 0:de.depthStencilTexture),e.setRenderTarget(w))}let he=C[lt];he===void 0&&(he=new tn,he.layers.enable(lt),he.viewport=new At,C[lt]=he),he.matrix.fromArray(tt.transform.matrix),he.matrix.decompose(he.position,he.quaternion,he.scale),he.projectionMatrix.fromArray(tt.projectionMatrix),he.projectionMatrixInverse.copy(he.projectionMatrix).invert(),he.viewport.set(ft.x,ft.y,ft.width,ft.height),lt===0&&(b.matrix.copy(he.matrix),b.matrix.decompose(b.position,b.quaternion,b.scale)),we===!0&&b.cameras.push(he)}const et=i.enabledFeatures;if(et&&et.includes("depth-sensing")){const lt=p.getDepthInformation(Ve[0]);lt&&lt.isValid&&lt.texture&&M.init(e,lt,i.renderState)}}for(let Ve=0;Ve<E.length;Ve++){const we=T[Ve],et=E[Ve];we!==null&&et!==void 0&&et.update(we,ge,h||l)}Se&&Se(se,ge),ge.detectedPlanes&&n.dispatchEvent({type:"planesdetected",data:ge}),y=null}const Je=new b_;Je.setAnimationLoop(Qe),this.setAnimationLoop=function(se){Se=se},this.dispose=function(){}}}const ls=new ai,ZT=new ut;function jT(r,e){function t(x,_){x.matrixAutoUpdate===!0&&x.updateMatrix(),_.value.copy(x.matrix)}function n(x,_){_.color.getRGB(x.fogColor.value,w_(r)),_.isFog?(x.fogNear.value=_.near,x.fogFar.value=_.far):_.isFogExp2&&(x.fogDensity.value=_.density)}function i(x,_,w,E,T){_.isMeshBasicMaterial||_.isMeshLambertMaterial?s(x,_):_.isMeshToonMaterial?(s(x,_),p(x,_)):_.isMeshPhongMaterial?(s(x,_),f(x,_)):_.isMeshStandardMaterial?(s(x,_),m(x,_),_.isMeshPhysicalMaterial&&g(x,_,T)):_.isMeshMatcapMaterial?(s(x,_),y(x,_)):_.isMeshDepthMaterial?s(x,_):_.isMeshDistanceMaterial?(s(x,_),M(x,_)):_.isMeshNormalMaterial?s(x,_):_.isLineBasicMaterial?(l(x,_),_.isLineDashedMaterial&&c(x,_)):_.isPointsMaterial?u(x,_,w,E):_.isSpriteMaterial?h(x,_):_.isShadowMaterial?(x.color.value.copy(_.color),x.opacity.value=_.opacity):_.isShaderMaterial&&(_.uniformsNeedUpdate=!1)}function s(x,_){x.opacity.value=_.opacity,_.color&&x.diffuse.value.copy(_.color),_.emissive&&x.emissive.value.copy(_.emissive).multiplyScalar(_.emissiveIntensity),_.map&&(x.map.value=_.map,t(_.map,x.mapTransform)),_.alphaMap&&(x.alphaMap.value=_.alphaMap,t(_.alphaMap,x.alphaMapTransform)),_.bumpMap&&(x.bumpMap.value=_.bumpMap,t(_.bumpMap,x.bumpMapTransform),x.bumpScale.value=_.bumpScale,_.side===Vn&&(x.bumpScale.value*=-1)),_.normalMap&&(x.normalMap.value=_.normalMap,t(_.normalMap,x.normalMapTransform),x.normalScale.value.copy(_.normalScale),_.side===Vn&&x.normalScale.value.negate()),_.displacementMap&&(x.displacementMap.value=_.displacementMap,t(_.displacementMap,x.displacementMapTransform),x.displacementScale.value=_.displacementScale,x.displacementBias.value=_.displacementBias),_.emissiveMap&&(x.emissiveMap.value=_.emissiveMap,t(_.emissiveMap,x.emissiveMapTransform)),_.specularMap&&(x.specularMap.value=_.specularMap,t(_.specularMap,x.specularMapTransform)),_.alphaTest>0&&(x.alphaTest.value=_.alphaTest);const w=e.get(_),E=w.envMap,T=w.envMapRotation;E&&(x.envMap.value=E,ls.copy(T),ls.x*=-1,ls.y*=-1,ls.z*=-1,E.isCubeTexture&&E.isRenderTargetTexture===!1&&(ls.y*=-1,ls.z*=-1),x.envMapRotation.value.setFromMatrix4(ZT.makeRotationFromEuler(ls)),x.flipEnvMap.value=E.isCubeTexture&&E.isRenderTargetTexture===!1?-1:1,x.reflectivity.value=_.reflectivity,x.ior.value=_.ior,x.refractionRatio.value=_.refractionRatio),_.lightMap&&(x.lightMap.value=_.lightMap,x.lightMapIntensity.value=_.lightMapIntensity,t(_.lightMap,x.lightMapTransform)),_.aoMap&&(x.aoMap.value=_.aoMap,x.aoMapIntensity.value=_.aoMapIntensity,t(_.aoMap,x.aoMapTransform))}function l(x,_){x.diffuse.value.copy(_.color),x.opacity.value=_.opacity,_.map&&(x.map.value=_.map,t(_.map,x.mapTransform))}function c(x,_){x.dashSize.value=_.dashSize,x.totalSize.value=_.dashSize+_.gapSize,x.scale.value=_.scale}function u(x,_,w,E){x.diffuse.value.copy(_.color),x.opacity.value=_.opacity,x.size.value=_.size*w,x.scale.value=E*.5,_.map&&(x.map.value=_.map,t(_.map,x.uvTransform)),_.alphaMap&&(x.alphaMap.value=_.alphaMap,t(_.alphaMap,x.alphaMapTransform)),_.alphaTest>0&&(x.alphaTest.value=_.alphaTest)}function h(x,_){x.diffuse.value.copy(_.color),x.opacity.value=_.opacity,x.rotation.value=_.rotation,_.map&&(x.map.value=_.map,t(_.map,x.mapTransform)),_.alphaMap&&(x.alphaMap.value=_.alphaMap,t(_.alphaMap,x.alphaMapTransform)),_.alphaTest>0&&(x.alphaTest.value=_.alphaTest)}function f(x,_){x.specular.value.copy(_.specular),x.shininess.value=Math.max(_.shininess,1e-4)}function p(x,_){_.gradientMap&&(x.gradientMap.value=_.gradientMap)}function m(x,_){x.metalness.value=_.metalness,_.metalnessMap&&(x.metalnessMap.value=_.metalnessMap,t(_.metalnessMap,x.metalnessMapTransform)),x.roughness.value=_.roughness,_.roughnessMap&&(x.roughnessMap.value=_.roughnessMap,t(_.roughnessMap,x.roughnessMapTransform)),_.envMap&&(x.envMapIntensity.value=_.envMapIntensity)}function g(x,_,w){x.ior.value=_.ior,_.sheen>0&&(x.sheenColor.value.copy(_.sheenColor).multiplyScalar(_.sheen),x.sheenRoughness.value=_.sheenRoughness,_.sheenColorMap&&(x.sheenColorMap.value=_.sheenColorMap,t(_.sheenColorMap,x.sheenColorMapTransform)),_.sheenRoughnessMap&&(x.sheenRoughnessMap.value=_.sheenRoughnessMap,t(_.sheenRoughnessMap,x.sheenRoughnessMapTransform))),_.clearcoat>0&&(x.clearcoat.value=_.clearcoat,x.clearcoatRoughness.value=_.clearcoatRoughness,_.clearcoatMap&&(x.clearcoatMap.value=_.clearcoatMap,t(_.clearcoatMap,x.clearcoatMapTransform)),_.clearcoatRoughnessMap&&(x.clearcoatRoughnessMap.value=_.clearcoatRoughnessMap,t(_.clearcoatRoughnessMap,x.clearcoatRoughnessMapTransform)),_.clearcoatNormalMap&&(x.clearcoatNormalMap.value=_.clearcoatNormalMap,t(_.clearcoatNormalMap,x.clearcoatNormalMapTransform),x.clearcoatNormalScale.value.copy(_.clearcoatNormalScale),_.side===Vn&&x.clearcoatNormalScale.value.negate())),_.dispersion>0&&(x.dispersion.value=_.dispersion),_.iridescence>0&&(x.iridescence.value=_.iridescence,x.iridescenceIOR.value=_.iridescenceIOR,x.iridescenceThicknessMinimum.value=_.iridescenceThicknessRange[0],x.iridescenceThicknessMaximum.value=_.iridescenceThicknessRange[1],_.iridescenceMap&&(x.iridescenceMap.value=_.iridescenceMap,t(_.iridescenceMap,x.iridescenceMapTransform)),_.iridescenceThicknessMap&&(x.iridescenceThicknessMap.value=_.iridescenceThicknessMap,t(_.iridescenceThicknessMap,x.iridescenceThicknessMapTransform))),_.transmission>0&&(x.transmission.value=_.transmission,x.transmissionSamplerMap.value=w.texture,x.transmissionSamplerSize.value.set(w.width,w.height),_.transmissionMap&&(x.transmissionMap.value=_.transmissionMap,t(_.transmissionMap,x.transmissionMapTransform)),x.thickness.value=_.thickness,_.thicknessMap&&(x.thicknessMap.value=_.thicknessMap,t(_.thicknessMap,x.thicknessMapTransform)),x.attenuationDistance.value=_.attenuationDistance,x.attenuationColor.value.copy(_.attenuationColor)),_.anisotropy>0&&(x.anisotropyVector.value.set(_.anisotropy*Math.cos(_.anisotropyRotation),_.anisotropy*Math.sin(_.anisotropyRotation)),_.anisotropyMap&&(x.anisotropyMap.value=_.anisotropyMap,t(_.anisotropyMap,x.anisotropyMapTransform))),x.specularIntensity.value=_.specularIntensity,x.specularColor.value.copy(_.specularColor),_.specularColorMap&&(x.specularColorMap.value=_.specularColorMap,t(_.specularColorMap,x.specularColorMapTransform)),_.specularIntensityMap&&(x.specularIntensityMap.value=_.specularIntensityMap,t(_.specularIntensityMap,x.specularIntensityMapTransform))}function y(x,_){_.matcap&&(x.matcap.value=_.matcap)}function M(x,_){const w=e.get(_).light;x.referencePosition.value.setFromMatrixPosition(w.matrixWorld),x.nearDistance.value=w.shadow.camera.near,x.farDistance.value=w.shadow.camera.far}return{refreshFogUniforms:n,refreshMaterialUniforms:i}}function JT(r,e,t,n){let i={},s={},l=[];const c=r.getParameter(r.MAX_UNIFORM_BUFFER_BINDINGS);function u(w,E){const T=E.program;n.uniformBlockBinding(w,T)}function h(w,E){let T=i[w.id];T===void 0&&(y(w),T=f(w),i[w.id]=T,w.addEventListener("dispose",x));const U=E.program;n.updateUBOMapping(w,U);const P=e.render.frame;s[w.id]!==P&&(m(w),s[w.id]=P)}function f(w){const E=p();w.__bindingPointIndex=E;const T=r.createBuffer(),U=w.__size,P=w.usage;return r.bindBuffer(r.UNIFORM_BUFFER,T),r.bufferData(r.UNIFORM_BUFFER,U,P),r.bindBuffer(r.UNIFORM_BUFFER,null),r.bindBufferBase(r.UNIFORM_BUFFER,E,T),T}function p(){for(let w=0;w<c;w++)if(l.indexOf(w)===-1)return l.push(w),w;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function m(w){const E=i[w.id],T=w.uniforms,U=w.__cache;r.bindBuffer(r.UNIFORM_BUFFER,E);for(let P=0,D=T.length;P<D;P++){const F=Array.isArray(T[P])?T[P]:[T[P]];for(let C=0,b=F.length;C<b;C++){const N=F[C];if(g(N,P,C,U)===!0){const q=N.__offset,Y=Array.isArray(N.value)?N.value:[N.value];let K=0;for(let le=0;le<Y.length;le++){const $=Y[le],pe=M($);typeof $=="number"||typeof $=="boolean"?(N.__data[0]=$,r.bufferSubData(r.UNIFORM_BUFFER,q+K,N.__data)):$.isMatrix3?(N.__data[0]=$.elements[0],N.__data[1]=$.elements[1],N.__data[2]=$.elements[2],N.__data[3]=0,N.__data[4]=$.elements[3],N.__data[5]=$.elements[4],N.__data[6]=$.elements[5],N.__data[7]=0,N.__data[8]=$.elements[6],N.__data[9]=$.elements[7],N.__data[10]=$.elements[8],N.__data[11]=0):($.toArray(N.__data,K),K+=pe.storage/Float32Array.BYTES_PER_ELEMENT)}r.bufferSubData(r.UNIFORM_BUFFER,q,N.__data)}}}r.bindBuffer(r.UNIFORM_BUFFER,null)}function g(w,E,T,U){const P=w.value,D=E+"_"+T;if(U[D]===void 0)return typeof P=="number"||typeof P=="boolean"?U[D]=P:U[D]=P.clone(),!0;{const F=U[D];if(typeof P=="number"||typeof P=="boolean"){if(F!==P)return U[D]=P,!0}else if(F.equals(P)===!1)return F.copy(P),!0}return!1}function y(w){const E=w.uniforms;let T=0;const U=16;for(let D=0,F=E.length;D<F;D++){const C=Array.isArray(E[D])?E[D]:[E[D]];for(let b=0,N=C.length;b<N;b++){const q=C[b],Y=Array.isArray(q.value)?q.value:[q.value];for(let K=0,le=Y.length;K<le;K++){const $=Y[K],pe=M($),J=T%U,xe=J%pe.boundary,me=J+xe;T+=xe,me!==0&&U-me<pe.storage&&(T+=U-me),q.__data=new Float32Array(pe.storage/Float32Array.BYTES_PER_ELEMENT),q.__offset=T,T+=pe.storage}}}const P=T%U;return P>0&&(T+=U-P),w.__size=T,w.__cache={},this}function M(w){const E={boundary:0,storage:0};return typeof w=="number"||typeof w=="boolean"?(E.boundary=4,E.storage=4):w.isVector2?(E.boundary=8,E.storage=8):w.isVector3||w.isColor?(E.boundary=16,E.storage=12):w.isVector4?(E.boundary=16,E.storage=16):w.isMatrix3?(E.boundary=48,E.storage=48):w.isMatrix4?(E.boundary=64,E.storage=64):w.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",w),E}function x(w){const E=w.target;E.removeEventListener("dispose",x);const T=l.indexOf(E.__bindingPointIndex);l.splice(T,1),r.deleteBuffer(i[E.id]),delete i[E.id],delete s[E.id]}function _(){for(const w in i)r.deleteBuffer(i[w]);l=[],i={},s={}}return{bind:u,update:h,dispose:_}}class U_{constructor(e={}){const{canvas:t=x_(),context:n=null,depth:i=!0,stencil:s=!1,alpha:l=!1,antialias:c=!1,premultipliedAlpha:u=!0,preserveDrawingBuffer:h=!1,powerPreference:f="default",failIfMajorPerformanceCaveat:p=!1,reverseDepthBuffer:m=!1}=e;this.isWebGLRenderer=!0;let g;if(n!==null){if(typeof WebGLRenderingContext<"u"&&n instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");g=n.getContextAttributes().alpha}else g=l;const y=new Uint32Array(4),M=new Int32Array(4);let x=null,_=null;const w=[],E=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=jn,this.toneMapping=qi,this.toneMappingExposure=1;const T=this;let U=!1,P=0,D=0,F=null,C=-1,b=null;const N=new At,q=new At;let Y=null;const K=new Be(0);let le=0,$=t.width,pe=t.height,J=1,xe=null,me=null;const Se=new At(0,0,$,pe),Qe=new At(0,0,$,pe);let Je=!1;const se=new nl;let ge=!1,Ve=!1;const we=new ut,et=new ut,lt=new L,tt=new At,ft={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let he=!1;function de(){return F===null?J:1}let z=n;function je(I,G){return t.getContext(I,G)}try{const I={alpha:!0,depth:i,stencil:s,antialias:c,premultipliedAlpha:u,preserveDrawingBuffer:h,powerPreference:f,failIfMajorPerformanceCaveat:p};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${Ja}`),t.addEventListener("webglcontextlost",ue,!1),t.addEventListener("webglcontextrestored",Ue,!1),t.addEventListener("webglcontextcreationerror",Ce,!1),z===null){const G="webgl2";if(z=je(G,I),z===null)throw je(G)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(I){throw console.error("THREE.WebGLRenderer: "+I.message),I}let ve,Oe,Te,it,Pe,O,R,Z,re,fe,ce,We,Ae,Fe,St,_e,He,rt,ct,ze,H,oe,Re,k;function ye(){ve=new n1(z),ve.init(),oe=new L_(z,ve),Oe=new Jw(z,ve,e,oe),Te=new OT(z,ve),Oe.reverseDepthBuffer&&m&&Te.buffers.depth.setReversed(!0),it=new s1(z),Pe=new ET,O=new VT(z,ve,Te,Pe,Oe,oe,it),R=new Qw(T),Z=new t1(T),re=new fM(z),Re=new Zw(z,re),fe=new i1(z,re,it,Re),ce=new a1(z,fe,re,it),ct=new o1(z,Oe,O),_e=new Kw(Pe),We=new MT(T,R,Z,ve,Oe,Re,_e),Ae=new jT(T,Pe),Fe=new TT,St=new IT(ve),rt=new qw(T,R,Z,Te,ce,g,u),He=new UT(T,ce,Oe),k=new JT(z,it,Oe,Te),ze=new jw(z,ve,it),H=new r1(z,ve,it),it.programs=We.programs,T.capabilities=Oe,T.extensions=ve,T.properties=Pe,T.renderLists=Fe,T.shadowMap=He,T.state=Te,T.info=it}ye();const te=new qT(T,z);this.xr=te,this.getContext=function(){return z},this.getContextAttributes=function(){return z.getContextAttributes()},this.forceContextLoss=function(){const I=ve.get("WEBGL_lose_context");I&&I.loseContext()},this.forceContextRestore=function(){const I=ve.get("WEBGL_lose_context");I&&I.restoreContext()},this.getPixelRatio=function(){return J},this.setPixelRatio=function(I){I!==void 0&&(J=I,this.setSize($,pe,!1))},this.getSize=function(I){return I.set($,pe)},this.setSize=function(I,G,Q=!0){if(te.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}$=I,pe=G,t.width=Math.floor(I*J),t.height=Math.floor(G*J),Q===!0&&(t.style.width=I+"px",t.style.height=G+"px"),this.setViewport(0,0,I,G)},this.getDrawingBufferSize=function(I){return I.set($*J,pe*J).floor()},this.setDrawingBufferSize=function(I,G,Q){$=I,pe=G,J=Q,t.width=Math.floor(I*Q),t.height=Math.floor(G*Q),this.setViewport(0,0,I,G)},this.getCurrentViewport=function(I){return I.copy(N)},this.getViewport=function(I){return I.copy(Se)},this.setViewport=function(I,G,Q,ee){I.isVector4?Se.set(I.x,I.y,I.z,I.w):Se.set(I,G,Q,ee),Te.viewport(N.copy(Se).multiplyScalar(J).round())},this.getScissor=function(I){return I.copy(Qe)},this.setScissor=function(I,G,Q,ee){I.isVector4?Qe.set(I.x,I.y,I.z,I.w):Qe.set(I,G,Q,ee),Te.scissor(q.copy(Qe).multiplyScalar(J).round())},this.getScissorTest=function(){return Je},this.setScissorTest=function(I){Te.setScissorTest(Je=I)},this.setOpaqueSort=function(I){xe=I},this.setTransparentSort=function(I){me=I},this.getClearColor=function(I){return I.copy(rt.getClearColor())},this.setClearColor=function(){rt.setClearColor.apply(rt,arguments)},this.getClearAlpha=function(){return rt.getClearAlpha()},this.setClearAlpha=function(){rt.setClearAlpha.apply(rt,arguments)},this.clear=function(I=!0,G=!0,Q=!0){let ee=0;if(I){let X=!1;if(F!==null){const Ee=F.texture.format;X=Ee===rh||Ee===ih||Ee===Qa}if(X){const Ee=F.texture.type,Ie=Ee===bi||Ee===yr||Ee===Io||Ee===Ls||Ee===eh||Ee===th,Xe=rt.getClearColor(),qe=rt.getClearAlpha(),ht=Xe.r,dt=Xe.g,Ze=Xe.b;Ie?(y[0]=ht,y[1]=dt,y[2]=Ze,y[3]=qe,z.clearBufferuiv(z.COLOR,0,y)):(M[0]=ht,M[1]=dt,M[2]=Ze,M[3]=qe,z.clearBufferiv(z.COLOR,0,M))}else ee|=z.COLOR_BUFFER_BIT}G&&(ee|=z.DEPTH_BUFFER_BIT),Q&&(ee|=z.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),z.clear(ee)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",ue,!1),t.removeEventListener("webglcontextrestored",Ue,!1),t.removeEventListener("webglcontextcreationerror",Ce,!1),Fe.dispose(),St.dispose(),Pe.dispose(),R.dispose(),Z.dispose(),ce.dispose(),Re.dispose(),k.dispose(),We.dispose(),te.dispose(),te.removeEventListener("sessionstart",cl),te.removeEventListener("sessionend",ul),Ii.stop()};function ue(I){I.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),U=!0}function Ue(){console.log("THREE.WebGLRenderer: Context Restored."),U=!1;const I=it.autoReset,G=He.enabled,Q=He.autoUpdate,ee=He.needsUpdate,X=He.type;ye(),it.autoReset=I,He.enabled=G,He.autoUpdate=Q,He.needsUpdate=ee,He.type=X}function Ce(I){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",I.statusMessage)}function nt(I){const G=I.target;G.removeEventListener("dispose",nt),It(G)}function It(I){Ht(I),Pe.remove(I)}function Ht(I){const G=Pe.get(I).programs;G!==void 0&&(G.forEach(function(Q){We.releaseProgram(Q)}),I.isShaderMaterial&&We.releaseShaderCache(I))}this.renderBufferDirect=function(I,G,Q,ee,X,Ee){G===null&&(G=ft);const Ie=X.isMesh&&X.matrixWorld.determinant()<0,Xe=Ch(I,G,Q,ee,X);Te.setMaterial(ee,Ie);let qe=Q.index,ht=1;if(ee.wireframe===!0){if(qe=fe.getWireframeAttribute(Q),qe===void 0)return;ht=2}const dt=Q.drawRange,Ze=Q.attributes.position;let Et=dt.start*ht,Rt=(dt.start+dt.count)*ht;Ee!==null&&(Et=Math.max(Et,Ee.start*ht),Rt=Math.min(Rt,(Ee.start+Ee.count)*ht)),qe!==null?(Et=Math.max(Et,0),Rt=Math.min(Rt,qe.count)):Ze!=null&&(Et=Math.max(Et,0),Rt=Math.min(Rt,Ze.count));const at=Rt-Et;if(at<0||at===1/0)return;Re.setup(X,ee,Xe,Q,qe);let _t,wt=ze;if(qe!==null&&(_t=re.get(qe),wt=H,wt.setIndex(_t)),X.isMesh)ee.wireframe===!0?(Te.setLineWidth(ee.wireframeLinewidth*de()),wt.setMode(z.LINES)):wt.setMode(z.TRIANGLES);else if(X.isLine){let De=ee.linewidth;De===void 0&&(De=1),Te.setLineWidth(De*de()),X.isLineSegments?wt.setMode(z.LINES):X.isLineLoop?wt.setMode(z.LINE_LOOP):wt.setMode(z.LINE_STRIP)}else X.isPoints?wt.setMode(z.POINTS):X.isSprite&&wt.setMode(z.TRIANGLES);if(X.isBatchedMesh)if(X._multiDrawInstances!==null)wt.renderMultiDrawInstances(X._multiDrawStarts,X._multiDrawCounts,X._multiDrawCount,X._multiDrawInstances);else if(ve.get("WEBGL_multi_draw"))wt.renderMultiDraw(X._multiDrawStarts,X._multiDrawCounts,X._multiDrawCount);else{const De=X._multiDrawStarts,Gt=X._multiDrawCounts,Ct=X._multiDrawCount,fn=qe?re.get(qe).bytesPerElement:1,Qt=Pe.get(ee).currentProgram.getUniforms();for(let dn=0;dn<Ct;dn++)Qt.setValue(z,"_gl_DrawID",dn),wt.render(De[dn]/fn,Gt[dn])}else if(X.isInstancedMesh)wt.renderInstances(Et,at,X.count);else if(Q.isInstancedBufferGeometry){const De=Q._maxInstanceCount!==void 0?Q._maxInstanceCount:1/0,Gt=Math.min(Q.instanceCount,De);wt.renderInstances(Et,at,Gt)}else wt.render(Et,at)};function bt(I,G,Q){I.transparent===!0&&I.side===Gi&&I.forceSinglePass===!1?(I.side=Vn,I.needsUpdate=!0,Vs(I,G,Q),I.side=vr,I.needsUpdate=!0,Vs(I,G,Q),I.side=Gi):Vs(I,G,Q)}this.compile=function(I,G,Q=null){Q===null&&(Q=I),_=St.get(Q),_.init(G),E.push(_),Q.traverseVisible(function(X){X.isLight&&X.layers.test(G.layers)&&(_.pushLight(X),X.castShadow&&_.pushShadow(X))}),I!==Q&&I.traverseVisible(function(X){X.isLight&&X.layers.test(G.layers)&&(_.pushLight(X),X.castShadow&&_.pushShadow(X))}),_.setupLights();const ee=new Set;return I.traverse(function(X){if(!(X.isMesh||X.isPoints||X.isLine||X.isSprite))return;const Ee=X.material;if(Ee)if(Array.isArray(Ee))for(let Ie=0;Ie<Ee.length;Ie++){const Xe=Ee[Ie];bt(Xe,Q,X),ee.add(Xe)}else bt(Ee,Q,X),ee.add(Ee)}),E.pop(),_=null,ee},this.compileAsync=function(I,G,Q=null){const ee=this.compile(I,G,Q);return new Promise(X=>{function Ee(){if(ee.forEach(function(Ie){Pe.get(Ie).currentProgram.isReady()&&ee.delete(Ie)}),ee.size===0){X(I);return}setTimeout(Ee,10)}ve.get("KHR_parallel_shader_compile")!==null?Ee():setTimeout(Ee,10)})};let rn=null;function Tn(I){rn&&rn(I)}function cl(){Ii.stop()}function ul(){Ii.start()}const Ii=new b_;Ii.setAnimationLoop(Tn),typeof self<"u"&&Ii.setContext(self),this.setAnimationLoop=function(I){rn=I,te.setAnimationLoop(I),I===null?Ii.stop():Ii.start()},te.addEventListener("sessionstart",cl),te.addEventListener("sessionend",ul),this.render=function(I,G){if(G!==void 0&&G.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(U===!0)return;if(I.matrixWorldAutoUpdate===!0&&I.updateMatrixWorld(),G.parent===null&&G.matrixWorldAutoUpdate===!0&&G.updateMatrixWorld(),te.enabled===!0&&te.isPresenting===!0&&(te.cameraAutoUpdate===!0&&te.updateCamera(G),G=te.getCamera()),I.isScene===!0&&I.onBeforeRender(T,I,G,F),_=St.get(I,E.length),_.init(G),E.push(_),et.multiplyMatrices(G.projectionMatrix,G.matrixWorldInverse),se.setFromProjectionMatrix(et),Ve=this.localClippingEnabled,ge=_e.init(this.clippingPlanes,Ve),x=Fe.get(I,w.length),x.init(),w.push(x),te.enabled===!0&&te.isPresenting===!0){const Ee=T.xr.getDepthSensingMesh();Ee!==null&&qr(Ee,G,-1/0,T.sortObjects)}qr(I,G,0,T.sortObjects),x.finish(),T.sortObjects===!0&&x.sort(xe,me),he=te.enabled===!1||te.isPresenting===!1||te.hasDepthSensing()===!1,he&&rt.addToRenderList(x,I),this.info.render.frame++,ge===!0&&_e.beginShadows();const Q=_.state.shadowsArray;He.render(Q,I,G),ge===!0&&_e.endShadows(),this.info.autoReset===!0&&this.info.reset();const ee=x.opaque,X=x.transmissive;if(_.setupLights(),G.isArrayCamera){const Ee=G.cameras;if(X.length>0)for(let Ie=0,Xe=Ee.length;Ie<Xe;Ie++){const qe=Ee[Ie];Sr(ee,X,I,qe)}he&&rt.render(I);for(let Ie=0,Xe=Ee.length;Ie<Xe;Ie++){const qe=Ee[Ie];hl(x,I,qe,qe.viewport)}}else X.length>0&&Sr(ee,X,I,G),he&&rt.render(I),hl(x,I,G);F!==null&&(O.updateMultisampleRenderTarget(F),O.updateRenderTargetMipmap(F)),I.isScene===!0&&I.onAfterRender(T,I,G),Re.resetDefaultState(),C=-1,b=null,E.pop(),E.length>0?(_=E[E.length-1],ge===!0&&_e.setGlobalState(T.clippingPlanes,_.state.camera)):_=null,w.pop(),w.length>0?x=w[w.length-1]:x=null};function qr(I,G,Q,ee){if(I.visible===!1)return;if(I.layers.test(G.layers)){if(I.isGroup)Q=I.renderOrder;else if(I.isLOD)I.autoUpdate===!0&&I.update(G);else if(I.isLight)_.pushLight(I),I.castShadow&&_.pushShadow(I);else if(I.isSprite){if(!I.frustumCulled||se.intersectsSprite(I)){ee&&tt.setFromMatrixPosition(I.matrixWorld).applyMatrix4(et);const Ie=ce.update(I),Xe=I.material;Xe.visible&&x.push(I,Ie,Xe,Q,tt.z,null)}}else if((I.isMesh||I.isLine||I.isPoints)&&(!I.frustumCulled||se.intersectsObject(I))){const Ie=ce.update(I),Xe=I.material;if(ee&&(I.boundingSphere!==void 0?(I.boundingSphere===null&&I.computeBoundingSphere(),tt.copy(I.boundingSphere.center)):(Ie.boundingSphere===null&&Ie.computeBoundingSphere(),tt.copy(Ie.boundingSphere.center)),tt.applyMatrix4(I.matrixWorld).applyMatrix4(et)),Array.isArray(Xe)){const qe=Ie.groups;for(let ht=0,dt=qe.length;ht<dt;ht++){const Ze=qe[ht],Et=Xe[Ze.materialIndex];Et&&Et.visible&&x.push(I,Ie,Et,Q,tt.z,Ze)}}else Xe.visible&&x.push(I,Ie,Xe,Q,tt.z,null)}}const Ee=I.children;for(let Ie=0,Xe=Ee.length;Ie<Xe;Ie++)qr(Ee[Ie],G,Q,ee)}function hl(I,G,Q,ee){const X=I.opaque,Ee=I.transmissive,Ie=I.transparent;_.setupLightsView(Q),ge===!0&&_e.setGlobalState(T.clippingPlanes,Q),ee&&Te.viewport(N.copy(ee)),X.length>0&&Hs(X,G,Q),Ee.length>0&&Hs(Ee,G,Q),Ie.length>0&&Hs(Ie,G,Q),Te.buffers.depth.setTest(!0),Te.buffers.depth.setMask(!0),Te.buffers.color.setMask(!0),Te.setPolygonOffset(!1)}function Sr(I,G,Q,ee){if((Q.isScene===!0?Q.overrideMaterial:null)!==null)return;_.state.transmissionRenderTarget[ee.id]===void 0&&(_.state.transmissionRenderTarget[ee.id]=new Ci(1,1,{generateMipmaps:!0,type:ve.has("EXT_color_buffer_half_float")||ve.has("EXT_color_buffer_float")?Fo:bi,minFilter:Xi,samples:4,stencilBuffer:s,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Pt.workingColorSpace}));const Ee=_.state.transmissionRenderTarget[ee.id],Ie=ee.viewport||N;Ee.setSize(Ie.z,Ie.w);const Xe=T.getRenderTarget();T.setRenderTarget(Ee),T.getClearColor(K),le=T.getClearAlpha(),le<1&&T.setClearColor(16777215,.5),T.clear(),he&&rt.render(Q);const qe=T.toneMapping;T.toneMapping=qi;const ht=ee.viewport;if(ee.viewport!==void 0&&(ee.viewport=void 0),_.setupLightsView(ee),ge===!0&&_e.setGlobalState(T.clippingPlanes,ee),Hs(I,Q,ee),O.updateMultisampleRenderTarget(Ee),O.updateRenderTargetMipmap(Ee),ve.has("WEBGL_multisampled_render_to_texture")===!1){let dt=!1;for(let Ze=0,Et=G.length;Ze<Et;Ze++){const Rt=G[Ze],at=Rt.object,_t=Rt.geometry,wt=Rt.material,De=Rt.group;if(wt.side===Gi&&at.layers.test(ee.layers)){const Gt=wt.side;wt.side=Vn,wt.needsUpdate=!0,fl(at,Q,ee,_t,wt,De),wt.side=Gt,wt.needsUpdate=!0,dt=!0}}dt===!0&&(O.updateMultisampleRenderTarget(Ee),O.updateRenderTargetMipmap(Ee))}T.setRenderTarget(Xe),T.setClearColor(K,le),ht!==void 0&&(ee.viewport=ht),T.toneMapping=qe}function Hs(I,G,Q){const ee=G.isScene===!0?G.overrideMaterial:null;for(let X=0,Ee=I.length;X<Ee;X++){const Ie=I[X],Xe=Ie.object,qe=Ie.geometry,ht=ee===null?Ie.material:ee,dt=Ie.group;Xe.layers.test(Q.layers)&&fl(Xe,G,Q,qe,ht,dt)}}function fl(I,G,Q,ee,X,Ee){I.onBeforeRender(T,G,Q,ee,X,Ee),I.modelViewMatrix.multiplyMatrices(Q.matrixWorldInverse,I.matrixWorld),I.normalMatrix.getNormalMatrix(I.modelViewMatrix),X.onBeforeRender(T,G,Q,ee,I,Ee),X.transparent===!0&&X.side===Gi&&X.forceSinglePass===!1?(X.side=Vn,X.needsUpdate=!0,T.renderBufferDirect(Q,G,ee,X,I,Ee),X.side=vr,X.needsUpdate=!0,T.renderBufferDirect(Q,G,ee,X,I,Ee),X.side=Gi):T.renderBufferDirect(Q,G,ee,X,I,Ee),I.onAfterRender(T,G,Q,ee,X,Ee)}function Vs(I,G,Q){G.isScene!==!0&&(G=ft);const ee=Pe.get(I),X=_.state.lights,Ee=_.state.shadowsArray,Ie=X.state.version,Xe=We.getParameters(I,X.state,Ee,G,Q),qe=We.getProgramCacheKey(Xe);let ht=ee.programs;ee.environment=I.isMeshStandardMaterial?G.environment:null,ee.fog=G.fog,ee.envMap=(I.isMeshStandardMaterial?Z:R).get(I.envMap||ee.environment),ee.envMapRotation=ee.environment!==null&&I.envMap===null?G.environmentRotation:I.envMapRotation,ht===void 0&&(I.addEventListener("dispose",nt),ht=new Map,ee.programs=ht);let dt=ht.get(qe);if(dt!==void 0){if(ee.currentProgram===dt&&ee.lightsStateVersion===Ie)return pl(I,Xe),dt}else Xe.uniforms=We.getUniforms(I),I.onBeforeCompile(Xe,T),dt=We.acquireProgram(Xe,qe),ht.set(qe,dt),ee.uniforms=Xe.uniforms;const Ze=ee.uniforms;return(!I.isShaderMaterial&&!I.isRawShaderMaterial||I.clipping===!0)&&(Ze.clippingPlanes=_e.uniform),pl(I,Xe),ee.needsLights=ml(I),ee.lightsStateVersion=Ie,ee.needsLights&&(Ze.ambientLightColor.value=X.state.ambient,Ze.lightProbe.value=X.state.probe,Ze.directionalLights.value=X.state.directional,Ze.directionalLightShadows.value=X.state.directionalShadow,Ze.spotLights.value=X.state.spot,Ze.spotLightShadows.value=X.state.spotShadow,Ze.rectAreaLights.value=X.state.rectArea,Ze.ltc_1.value=X.state.rectAreaLTC1,Ze.ltc_2.value=X.state.rectAreaLTC2,Ze.pointLights.value=X.state.point,Ze.pointLightShadows.value=X.state.pointShadow,Ze.hemisphereLights.value=X.state.hemi,Ze.directionalShadowMap.value=X.state.directionalShadowMap,Ze.directionalShadowMatrix.value=X.state.directionalShadowMatrix,Ze.spotShadowMap.value=X.state.spotShadowMap,Ze.spotLightMatrix.value=X.state.spotLightMatrix,Ze.spotLightMap.value=X.state.spotLightMap,Ze.pointShadowMap.value=X.state.pointShadowMap,Ze.pointShadowMatrix.value=X.state.pointShadowMatrix),ee.currentProgram=dt,ee.uniformsList=null,dt}function dl(I){if(I.uniformsList===null){const G=I.currentProgram.getUniforms();I.uniformsList=au.seqWithValue(G.seq,I.uniforms)}return I.uniformsList}function pl(I,G){const Q=Pe.get(I);Q.outputColorSpace=G.outputColorSpace,Q.batching=G.batching,Q.batchingColor=G.batchingColor,Q.instancing=G.instancing,Q.instancingColor=G.instancingColor,Q.instancingMorph=G.instancingMorph,Q.skinning=G.skinning,Q.morphTargets=G.morphTargets,Q.morphNormals=G.morphNormals,Q.morphColors=G.morphColors,Q.morphTargetsCount=G.morphTargetsCount,Q.numClippingPlanes=G.numClippingPlanes,Q.numIntersection=G.numClipIntersection,Q.vertexAlphas=G.vertexAlphas,Q.vertexTangents=G.vertexTangents,Q.toneMapping=G.toneMapping}function Ch(I,G,Q,ee,X){G.isScene!==!0&&(G=ft),O.resetTextureUnits();const Ee=G.fog,Ie=ee.isMeshStandardMaterial?G.environment:null,Xe=F===null?T.outputColorSpace:F.isXRRenderTarget===!0?F.texture.colorSpace:Ns,qe=(ee.isMeshStandardMaterial?Z:R).get(ee.envMap||Ie),ht=ee.vertexColors===!0&&!!Q.attributes.color&&Q.attributes.color.itemSize===4,dt=!!Q.attributes.tangent&&(!!ee.normalMap||ee.anisotropy>0),Ze=!!Q.morphAttributes.position,Et=!!Q.morphAttributes.normal,Rt=!!Q.morphAttributes.color;let at=qi;ee.toneMapped&&(F===null||F.isXRRenderTarget===!0)&&(at=T.toneMapping);const _t=Q.morphAttributes.position||Q.morphAttributes.normal||Q.morphAttributes.color,wt=_t!==void 0?_t.length:0,De=Pe.get(ee),Gt=_.state.lights;if(ge===!0&&(Ve===!0||I!==b)){const Wt=I===b&&ee.id===C;_e.setState(ee,I,Wt)}let Ct=!1;ee.version===De.__version?(De.needsLights&&De.lightsStateVersion!==Gt.state.version||De.outputColorSpace!==Xe||X.isBatchedMesh&&De.batching===!1||!X.isBatchedMesh&&De.batching===!0||X.isBatchedMesh&&De.batchingColor===!0&&X.colorTexture===null||X.isBatchedMesh&&De.batchingColor===!1&&X.colorTexture!==null||X.isInstancedMesh&&De.instancing===!1||!X.isInstancedMesh&&De.instancing===!0||X.isSkinnedMesh&&De.skinning===!1||!X.isSkinnedMesh&&De.skinning===!0||X.isInstancedMesh&&De.instancingColor===!0&&X.instanceColor===null||X.isInstancedMesh&&De.instancingColor===!1&&X.instanceColor!==null||X.isInstancedMesh&&De.instancingMorph===!0&&X.morphTexture===null||X.isInstancedMesh&&De.instancingMorph===!1&&X.morphTexture!==null||De.envMap!==qe||ee.fog===!0&&De.fog!==Ee||De.numClippingPlanes!==void 0&&(De.numClippingPlanes!==_e.numPlanes||De.numIntersection!==_e.numIntersection)||De.vertexAlphas!==ht||De.vertexTangents!==dt||De.morphTargets!==Ze||De.morphNormals!==Et||De.morphColors!==Rt||De.toneMapping!==at||De.morphTargetsCount!==wt)&&(Ct=!0):(Ct=!0,De.__version=ee.version);let fn=De.currentProgram;Ct===!0&&(fn=Vs(ee,G,X));let Qt=!1,dn=!1,Mr=!1;const Bt=fn.getUniforms(),On=De.uniforms;if(Te.useProgram(fn.program)&&(Qt=!0,dn=!0,Mr=!0),ee.id!==C&&(C=ee.id,dn=!0),Qt||b!==I){Te.buffers.depth.getReversed()?(we.copy(I.projectionMatrix),FS(we),BS(we),Bt.setValue(z,"projectionMatrix",we)):Bt.setValue(z,"projectionMatrix",I.projectionMatrix),Bt.setValue(z,"viewMatrix",I.matrixWorldInverse);const Li=Bt.map.cameraPosition;Li!==void 0&&Li.setValue(z,lt.setFromMatrixPosition(I.matrixWorld)),Oe.logarithmicDepthBuffer&&Bt.setValue(z,"logDepthBufFC",2/(Math.log(I.far+1)/Math.LN2)),(ee.isMeshPhongMaterial||ee.isMeshToonMaterial||ee.isMeshLambertMaterial||ee.isMeshBasicMaterial||ee.isMeshStandardMaterial||ee.isShaderMaterial)&&Bt.setValue(z,"isOrthographic",I.isOrthographicCamera===!0),b!==I&&(b=I,dn=!0,Mr=!0)}if(X.isSkinnedMesh){Bt.setOptional(z,X,"bindMatrix"),Bt.setOptional(z,X,"bindMatrixInverse");const Wt=X.skeleton;Wt&&(Wt.boneTexture===null&&Wt.computeBoneTexture(),Bt.setValue(z,"boneTexture",Wt.boneTexture,O))}X.isBatchedMesh&&(Bt.setOptional(z,X,"batchingTexture"),Bt.setValue(z,"batchingTexture",X._matricesTexture,O),Bt.setOptional(z,X,"batchingIdTexture"),Bt.setValue(z,"batchingIdTexture",X._indirectTexture,O),Bt.setOptional(z,X,"batchingColorTexture"),X._colorsTexture!==null&&Bt.setValue(z,"batchingColorTexture",X._colorsTexture,O));const Er=Q.morphAttributes;if((Er.position!==void 0||Er.normal!==void 0||Er.color!==void 0)&&ct.update(X,Q,fn),(dn||De.receiveShadow!==X.receiveShadow)&&(De.receiveShadow=X.receiveShadow,Bt.setValue(z,"receiveShadow",X.receiveShadow)),ee.isMeshGouraudMaterial&&ee.envMap!==null&&(On.envMap.value=qe,On.flipEnvMap.value=qe.isCubeTexture&&qe.isRenderTargetTexture===!1?-1:1),ee.isMeshStandardMaterial&&ee.envMap===null&&G.environment!==null&&(On.envMapIntensity.value=G.environmentIntensity),dn&&(Bt.setValue(z,"toneMappingExposure",T.toneMappingExposure),De.needsLights&&Rh(On,Mr),Ee&&ee.fog===!0&&Ae.refreshFogUniforms(On,Ee),Ae.refreshMaterialUniforms(On,ee,J,pe,_.state.transmissionRenderTarget[I.id]),au.upload(z,dl(De),On,O)),ee.isShaderMaterial&&ee.uniformsNeedUpdate===!0&&(au.upload(z,dl(De),On,O),ee.uniformsNeedUpdate=!1),ee.isSpriteMaterial&&Bt.setValue(z,"center",X.center),Bt.setValue(z,"modelViewMatrix",X.modelViewMatrix),Bt.setValue(z,"normalMatrix",X.normalMatrix),Bt.setValue(z,"modelMatrix",X.matrixWorld),ee.isShaderMaterial||ee.isRawShaderMaterial){const Wt=ee.uniformsGroups;for(let Li=0,Di=Wt.length;Li<Di;Li++){const gl=Wt[Li];k.update(gl,fn),k.bind(gl,fn)}}return fn}function Rh(I,G){I.ambientLightColor.needsUpdate=G,I.lightProbe.needsUpdate=G,I.directionalLights.needsUpdate=G,I.directionalLightShadows.needsUpdate=G,I.pointLights.needsUpdate=G,I.pointLightShadows.needsUpdate=G,I.spotLights.needsUpdate=G,I.spotLightShadows.needsUpdate=G,I.rectAreaLights.needsUpdate=G,I.hemisphereLights.needsUpdate=G}function ml(I){return I.isMeshLambertMaterial||I.isMeshToonMaterial||I.isMeshPhongMaterial||I.isMeshStandardMaterial||I.isShadowMaterial||I.isShaderMaterial&&I.lights===!0}this.getActiveCubeFace=function(){return P},this.getActiveMipmapLevel=function(){return D},this.getRenderTarget=function(){return F},this.setRenderTargetTextures=function(I,G,Q){Pe.get(I.texture).__webglTexture=G,Pe.get(I.depthTexture).__webglTexture=Q;const ee=Pe.get(I);ee.__hasExternalTextures=!0,ee.__autoAllocateDepthBuffer=Q===void 0,ee.__autoAllocateDepthBuffer||ve.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),ee.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(I,G){const Q=Pe.get(I);Q.__webglFramebuffer=G,Q.__useDefaultFramebuffer=G===void 0},this.setRenderTarget=function(I,G=0,Q=0){F=I,P=G,D=Q;let ee=!0,X=null,Ee=!1,Ie=!1;if(I){const qe=Pe.get(I);if(qe.__useDefaultFramebuffer!==void 0)Te.bindFramebuffer(z.FRAMEBUFFER,null),ee=!1;else if(qe.__webglFramebuffer===void 0)O.setupRenderTarget(I);else if(qe.__hasExternalTextures)O.rebindTextures(I,Pe.get(I.texture).__webglTexture,Pe.get(I.depthTexture).__webglTexture);else if(I.depthBuffer){const Ze=I.depthTexture;if(qe.__boundDepthTexture!==Ze){if(Ze!==null&&Pe.has(Ze)&&(I.width!==Ze.image.width||I.height!==Ze.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");O.setupDepthRenderbuffer(I)}}const ht=I.texture;(ht.isData3DTexture||ht.isDataArrayTexture||ht.isCompressedArrayTexture)&&(Ie=!0);const dt=Pe.get(I).__webglFramebuffer;I.isWebGLCubeRenderTarget?(Array.isArray(dt[G])?X=dt[G][Q]:X=dt[G],Ee=!0):I.samples>0&&O.useMultisampledRTT(I)===!1?X=Pe.get(I).__webglMultisampledFramebuffer:Array.isArray(dt)?X=dt[Q]:X=dt,N.copy(I.viewport),q.copy(I.scissor),Y=I.scissorTest}else N.copy(Se).multiplyScalar(J).floor(),q.copy(Qe).multiplyScalar(J).floor(),Y=Je;if(Te.bindFramebuffer(z.FRAMEBUFFER,X)&&ee&&Te.drawBuffers(I,X),Te.viewport(N),Te.scissor(q),Te.setScissorTest(Y),Ee){const qe=Pe.get(I.texture);z.framebufferTexture2D(z.FRAMEBUFFER,z.COLOR_ATTACHMENT0,z.TEXTURE_CUBE_MAP_POSITIVE_X+G,qe.__webglTexture,Q)}else if(Ie){const qe=Pe.get(I.texture),ht=G||0;z.framebufferTextureLayer(z.FRAMEBUFFER,z.COLOR_ATTACHMENT0,qe.__webglTexture,Q||0,ht)}C=-1},this.readRenderTargetPixels=function(I,G,Q,ee,X,Ee,Ie){if(!(I&&I.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Xe=Pe.get(I).__webglFramebuffer;if(I.isWebGLCubeRenderTarget&&Ie!==void 0&&(Xe=Xe[Ie]),Xe){Te.bindFramebuffer(z.FRAMEBUFFER,Xe);try{const qe=I.texture,ht=qe.format,dt=qe.type;if(!Oe.textureFormatReadable(ht)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Oe.textureTypeReadable(dt)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}G>=0&&G<=I.width-ee&&Q>=0&&Q<=I.height-X&&z.readPixels(G,Q,ee,X,oe.convert(ht),oe.convert(dt),Ee)}finally{const qe=F!==null?Pe.get(F).__webglFramebuffer:null;Te.bindFramebuffer(z.FRAMEBUFFER,qe)}}},this.readRenderTargetPixelsAsync=async function(I,G,Q,ee,X,Ee,Ie){if(!(I&&I.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Xe=Pe.get(I).__webglFramebuffer;if(I.isWebGLCubeRenderTarget&&Ie!==void 0&&(Xe=Xe[Ie]),Xe){const qe=I.texture,ht=qe.format,dt=qe.type;if(!Oe.textureFormatReadable(ht))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Oe.textureTypeReadable(dt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(G>=0&&G<=I.width-ee&&Q>=0&&Q<=I.height-X){Te.bindFramebuffer(z.FRAMEBUFFER,Xe);const Ze=z.createBuffer();z.bindBuffer(z.PIXEL_PACK_BUFFER,Ze),z.bufferData(z.PIXEL_PACK_BUFFER,Ee.byteLength,z.STREAM_READ),z.readPixels(G,Q,ee,X,oe.convert(ht),oe.convert(dt),0);const Et=F!==null?Pe.get(F).__webglFramebuffer:null;Te.bindFramebuffer(z.FRAMEBUFFER,Et);const Rt=z.fenceSync(z.SYNC_GPU_COMMANDS_COMPLETE,0);return z.flush(),await OS(z,Rt,4),z.bindBuffer(z.PIXEL_PACK_BUFFER,Ze),z.getBufferSubData(z.PIXEL_PACK_BUFFER,0,Ee),z.deleteBuffer(Ze),z.deleteSync(Rt),Ee}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(I,G=null,Q=0){I.isTexture!==!0&&(xa("WebGLRenderer: copyFramebufferToTexture function signature has changed."),G=arguments[0]||null,I=arguments[1]);const ee=Math.pow(2,-Q),X=Math.floor(I.image.width*ee),Ee=Math.floor(I.image.height*ee),Ie=G!==null?G.x:0,Xe=G!==null?G.y:0;O.setTexture2D(I,0),z.copyTexSubImage2D(z.TEXTURE_2D,Q,0,0,Ie,Xe,X,Ee),Te.unbindTexture()},this.copyTextureToTexture=function(I,G,Q=null,ee=null,X=0){I.isTexture!==!0&&(xa("WebGLRenderer: copyTextureToTexture function signature has changed."),ee=arguments[0]||null,I=arguments[1],G=arguments[2],X=arguments[3]||0,Q=null);let Ee,Ie,Xe,qe,ht,dt,Ze,Et,Rt;const at=I.isCompressedTexture?I.mipmaps[X]:I.image;Q!==null?(Ee=Q.max.x-Q.min.x,Ie=Q.max.y-Q.min.y,Xe=Q.isBox3?Q.max.z-Q.min.z:1,qe=Q.min.x,ht=Q.min.y,dt=Q.isBox3?Q.min.z:0):(Ee=at.width,Ie=at.height,Xe=at.depth||1,qe=0,ht=0,dt=0),ee!==null?(Ze=ee.x,Et=ee.y,Rt=ee.z):(Ze=0,Et=0,Rt=0);const _t=oe.convert(G.format),wt=oe.convert(G.type);let De;G.isData3DTexture?(O.setTexture3D(G,0),De=z.TEXTURE_3D):G.isDataArrayTexture||G.isCompressedArrayTexture?(O.setTexture2DArray(G,0),De=z.TEXTURE_2D_ARRAY):(O.setTexture2D(G,0),De=z.TEXTURE_2D),z.pixelStorei(z.UNPACK_FLIP_Y_WEBGL,G.flipY),z.pixelStorei(z.UNPACK_PREMULTIPLY_ALPHA_WEBGL,G.premultiplyAlpha),z.pixelStorei(z.UNPACK_ALIGNMENT,G.unpackAlignment);const Gt=z.getParameter(z.UNPACK_ROW_LENGTH),Ct=z.getParameter(z.UNPACK_IMAGE_HEIGHT),fn=z.getParameter(z.UNPACK_SKIP_PIXELS),Qt=z.getParameter(z.UNPACK_SKIP_ROWS),dn=z.getParameter(z.UNPACK_SKIP_IMAGES);z.pixelStorei(z.UNPACK_ROW_LENGTH,at.width),z.pixelStorei(z.UNPACK_IMAGE_HEIGHT,at.height),z.pixelStorei(z.UNPACK_SKIP_PIXELS,qe),z.pixelStorei(z.UNPACK_SKIP_ROWS,ht),z.pixelStorei(z.UNPACK_SKIP_IMAGES,dt);const Mr=I.isDataArrayTexture||I.isData3DTexture,Bt=G.isDataArrayTexture||G.isData3DTexture;if(I.isRenderTargetTexture||I.isDepthTexture){const On=Pe.get(I),Er=Pe.get(G),Wt=Pe.get(On.__renderTarget),Li=Pe.get(Er.__renderTarget);Te.bindFramebuffer(z.READ_FRAMEBUFFER,Wt.__webglFramebuffer),Te.bindFramebuffer(z.DRAW_FRAMEBUFFER,Li.__webglFramebuffer);for(let Di=0;Di<Xe;Di++)Mr&&z.framebufferTextureLayer(z.READ_FRAMEBUFFER,z.COLOR_ATTACHMENT0,Pe.get(I).__webglTexture,X,dt+Di),I.isDepthTexture?(Bt&&z.framebufferTextureLayer(z.DRAW_FRAMEBUFFER,z.COLOR_ATTACHMENT0,Pe.get(G).__webglTexture,X,Rt+Di),z.blitFramebuffer(qe,ht,Ee,Ie,Ze,Et,Ee,Ie,z.DEPTH_BUFFER_BIT,z.NEAREST)):Bt?z.copyTexSubImage3D(De,X,Ze,Et,Rt+Di,qe,ht,Ee,Ie):z.copyTexSubImage2D(De,X,Ze,Et,Rt+Di,qe,ht,Ee,Ie);Te.bindFramebuffer(z.READ_FRAMEBUFFER,null),Te.bindFramebuffer(z.DRAW_FRAMEBUFFER,null)}else Bt?I.isDataTexture||I.isData3DTexture?z.texSubImage3D(De,X,Ze,Et,Rt,Ee,Ie,Xe,_t,wt,at.data):G.isCompressedArrayTexture?z.compressedTexSubImage3D(De,X,Ze,Et,Rt,Ee,Ie,Xe,_t,at.data):z.texSubImage3D(De,X,Ze,Et,Rt,Ee,Ie,Xe,_t,wt,at):I.isDataTexture?z.texSubImage2D(z.TEXTURE_2D,X,Ze,Et,Ee,Ie,_t,wt,at.data):I.isCompressedTexture?z.compressedTexSubImage2D(z.TEXTURE_2D,X,Ze,Et,at.width,at.height,_t,at.data):z.texSubImage2D(z.TEXTURE_2D,X,Ze,Et,Ee,Ie,_t,wt,at);z.pixelStorei(z.UNPACK_ROW_LENGTH,Gt),z.pixelStorei(z.UNPACK_IMAGE_HEIGHT,Ct),z.pixelStorei(z.UNPACK_SKIP_PIXELS,fn),z.pixelStorei(z.UNPACK_SKIP_ROWS,Qt),z.pixelStorei(z.UNPACK_SKIP_IMAGES,dn),X===0&&G.generateMipmaps&&z.generateMipmap(De),Te.unbindTexture()},this.copyTextureToTexture3D=function(I,G,Q=null,ee=null,X=0){return I.isTexture!==!0&&(xa("WebGLRenderer: copyTextureToTexture3D function signature has changed."),Q=arguments[0]||null,ee=arguments[1]||null,I=arguments[2],G=arguments[3],X=arguments[4]||0),xa('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(I,G,Q,ee,X)},this.initRenderTarget=function(I){Pe.get(I).__webglFramebuffer===void 0&&O.setupRenderTarget(I)},this.initTexture=function(I){I.isCubeTexture?O.setTextureCube(I,0):I.isData3DTexture?O.setTexture3D(I,0):I.isDataArrayTexture||I.isCompressedArrayTexture?O.setTexture2DArray(I,0):O.setTexture2D(I,0),Te.unbindTexture()},this.resetState=function(){P=0,D=0,F=null,Te.reset(),Re.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return Yi}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Pt._getDrawingBufferColorSpace(e),t.unpackColorSpace=Pt._getUnpackColorSpace()}}class lh{constructor(e,t=25e-5){this.isFogExp2=!0,this.name="",this.color=new Be(e),this.density=t}clone(){return new lh(this.color,this.density)}toJSON(){return{type:"FogExp2",name:this.name,color:this.color.getHex(),density:this.density}}}class ch{constructor(e,t=1,n=1e3){this.isFog=!0,this.name="",this.color=new Be(e),this.near=t,this.far=n}clone(){return new ch(this.color,this.near,this.far)}toJSON(){return{type:"Fog",name:this.name,color:this.color.getHex(),near:this.near,far:this.far}}}class Mp extends Dt{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new ai,this.environmentIntensity=1,this.environmentRotation=new ai,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}class uh{constructor(e,t){this.isInterleavedBuffer=!0,this.array=e,this.stride=t,this.count=e!==void 0?e.length/t:0,this.usage=za,this.updateRanges=[],this.version=0,this.uuid=oi()}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.array=new e.array.constructor(e.array),this.count=e.count,this.stride=e.stride,this.usage=e.usage,this}copyAt(e,t,n){e*=this.stride,n*=t.stride;for(let i=0,s=this.stride;i<s;i++)this.array[e+i]=t.array[n+i];return this}set(e,t=0){return this.array.set(e,t),this}clone(e){e.arrayBuffers===void 0&&(e.arrayBuffers={}),this.array.buffer._uuid===void 0&&(this.array.buffer._uuid=oi()),e.arrayBuffers[this.array.buffer._uuid]===void 0&&(e.arrayBuffers[this.array.buffer._uuid]=this.array.slice(0).buffer);const t=new this.array.constructor(e.arrayBuffers[this.array.buffer._uuid]),n=new this.constructor(t,this.stride);return n.setUsage(this.usage),n}onUpload(e){return this.onUploadCallback=e,this}toJSON(e){return e.arrayBuffers===void 0&&(e.arrayBuffers={}),this.array.buffer._uuid===void 0&&(this.array.buffer._uuid=oi()),e.arrayBuffers[this.array.buffer._uuid]===void 0&&(e.arrayBuffers[this.array.buffer._uuid]=Array.from(new Uint32Array(this.array.buffer))),{uuid:this.uuid,buffer:this.array.buffer._uuid,type:this.array.constructor.name,stride:this.stride}}}const zn=new L;class si{constructor(e,t,n,i=!1){this.isInterleavedBufferAttribute=!0,this.name="",this.data=e,this.itemSize=t,this.offset=n,this.normalized=i}get count(){return this.data.count}get array(){return this.data.array}set needsUpdate(e){this.data.needsUpdate=e}applyMatrix4(e){for(let t=0,n=this.data.count;t<n;t++)zn.fromBufferAttribute(this,t),zn.applyMatrix4(e),this.setXYZ(t,zn.x,zn.y,zn.z);return this}applyNormalMatrix(e){for(let t=0,n=this.count;t<n;t++)zn.fromBufferAttribute(this,t),zn.applyNormalMatrix(e),this.setXYZ(t,zn.x,zn.y,zn.z);return this}transformDirection(e){for(let t=0,n=this.count;t<n;t++)zn.fromBufferAttribute(this,t),zn.transformDirection(e),this.setXYZ(t,zn.x,zn.y,zn.z);return this}getComponent(e,t){let n=this.array[e*this.data.stride+this.offset+t];return this.normalized&&(n=Hn(n,this.array)),n}setComponent(e,t,n){return this.normalized&&(n=vt(n,this.array)),this.data.array[e*this.data.stride+this.offset+t]=n,this}setX(e,t){return this.normalized&&(t=vt(t,this.array)),this.data.array[e*this.data.stride+this.offset]=t,this}setY(e,t){return this.normalized&&(t=vt(t,this.array)),this.data.array[e*this.data.stride+this.offset+1]=t,this}setZ(e,t){return this.normalized&&(t=vt(t,this.array)),this.data.array[e*this.data.stride+this.offset+2]=t,this}setW(e,t){return this.normalized&&(t=vt(t,this.array)),this.data.array[e*this.data.stride+this.offset+3]=t,this}getX(e){let t=this.data.array[e*this.data.stride+this.offset];return this.normalized&&(t=Hn(t,this.array)),t}getY(e){let t=this.data.array[e*this.data.stride+this.offset+1];return this.normalized&&(t=Hn(t,this.array)),t}getZ(e){let t=this.data.array[e*this.data.stride+this.offset+2];return this.normalized&&(t=Hn(t,this.array)),t}getW(e){let t=this.data.array[e*this.data.stride+this.offset+3];return this.normalized&&(t=Hn(t,this.array)),t}setXY(e,t,n){return e=e*this.data.stride+this.offset,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=n,this}setXYZ(e,t,n,i){return e=e*this.data.stride+this.offset,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=n,this.data.array[e+2]=i,this}setXYZW(e,t,n,i,s){return e=e*this.data.stride+this.offset,this.normalized&&(t=vt(t,this.array),n=vt(n,this.array),i=vt(i,this.array),s=vt(s,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=n,this.data.array[e+2]=i,this.data.array[e+3]=s,this}clone(e){if(e===void 0){console.log("THREE.InterleavedBufferAttribute.clone(): Cloning an interleaved buffer attribute will de-interleave buffer data.");const t=[];for(let n=0;n<this.count;n++){const i=n*this.data.stride+this.offset;for(let s=0;s<this.itemSize;s++)t.push(this.data.array[i+s])}return new zt(new this.array.constructor(t),this.itemSize,this.normalized)}else return e.interleavedBuffers===void 0&&(e.interleavedBuffers={}),e.interleavedBuffers[this.data.uuid]===void 0&&(e.interleavedBuffers[this.data.uuid]=this.data.clone(e)),new si(e.interleavedBuffers[this.data.uuid],this.itemSize,this.offset,this.normalized)}toJSON(e){if(e===void 0){console.log("THREE.InterleavedBufferAttribute.toJSON(): Serializing an interleaved buffer attribute will de-interleave buffer data.");const t=[];for(let n=0;n<this.count;n++){const i=n*this.data.stride+this.offset;for(let s=0;s<this.itemSize;s++)t.push(this.data.array[i+s])}return{itemSize:this.itemSize,type:this.array.constructor.name,array:t,normalized:this.normalized}}else return e.interleavedBuffers===void 0&&(e.interleavedBuffers={}),e.interleavedBuffers[this.data.uuid]===void 0&&(e.interleavedBuffers[this.data.uuid]=this.data.toJSON(e)),{isInterleavedBufferAttribute:!0,itemSize:this.itemSize,data:this.data.uuid,offset:this.offset,normalized:this.normalized}}}class Ep extends Nn{static get type(){return"SpriteMaterial"}constructor(e){super(),this.isSpriteMaterial=!0,this.color=new Be(16777215),this.map=null,this.alphaMap=null,this.rotation=0,this.sizeAttenuation=!0,this.transparent=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.alphaMap=e.alphaMap,this.rotation=e.rotation,this.sizeAttenuation=e.sizeAttenuation,this.fog=e.fog,this}}let mo;const ua=new L,go=new L,vo=new L,_o=new ae,ha=new ae,N_=new ut,Rc=new L,fa=new L,Pc=new L,v0=new ae,ld=new ae,_0=new ae;class O_ extends Dt{constructor(e=new Ep){if(super(),this.isSprite=!0,this.type="Sprite",mo===void 0){mo=new xt;const t=new Float32Array([-.5,-.5,0,0,0,.5,-.5,0,1,0,.5,.5,0,1,1,-.5,.5,0,0,1]),n=new uh(t,5);mo.setIndex([0,1,2,0,2,3]),mo.setAttribute("position",new si(n,3,0,!1)),mo.setAttribute("uv",new si(n,2,3,!1))}this.geometry=mo,this.material=e,this.center=new ae(.5,.5)}raycast(e,t){e.camera===null&&console.error('THREE.Sprite: "Raycaster.camera" needs to be set in order to raycast against sprites.'),go.setFromMatrixScale(this.matrixWorld),N_.copy(e.camera.matrixWorld),this.modelViewMatrix.multiplyMatrices(e.camera.matrixWorldInverse,this.matrixWorld),vo.setFromMatrixPosition(this.modelViewMatrix),e.camera.isPerspectiveCamera&&this.material.sizeAttenuation===!1&&go.multiplyScalar(-vo.z);const n=this.material.rotation;let i,s;n!==0&&(s=Math.cos(n),i=Math.sin(n));const l=this.center;Ic(Rc.set(-.5,-.5,0),vo,l,go,i,s),Ic(fa.set(.5,-.5,0),vo,l,go,i,s),Ic(Pc.set(.5,.5,0),vo,l,go,i,s),v0.set(0,0),ld.set(1,0),_0.set(1,1);let c=e.ray.intersectTriangle(Rc,fa,Pc,!1,ua);if(c===null&&(Ic(fa.set(-.5,.5,0),vo,l,go,i,s),ld.set(0,1),c=e.ray.intersectTriangle(Rc,Pc,fa,!1,ua),c===null))return;const u=e.ray.origin.distanceTo(ua);u<e.near||u>e.far||t.push({distance:u,point:ua.clone(),uv:Jn.getInterpolation(ua,Rc,fa,Pc,v0,ld,_0,new ae),face:null,object:this})}copy(e,t){return super.copy(e,t),e.center!==void 0&&this.center.copy(e.center),this.material=e.material,this}}function Ic(r,e,t,n,i,s){_o.subVectors(r,t).addScalar(.5).multiply(n),i!==void 0?(ha.x=s*_o.x-i*_o.y,ha.y=i*_o.x+s*_o.y):ha.copy(_o),r.copy(e),r.x+=ha.x,r.y+=ha.y,r.applyMatrix4(N_)}const Lc=new L,y0=new L;class F_ extends Dt{constructor(){super(),this._currentLevel=0,this.type="LOD",Object.defineProperties(this,{levels:{enumerable:!0,value:[]},isLOD:{value:!0}}),this.autoUpdate=!0}copy(e){super.copy(e,!1);const t=e.levels;for(let n=0,i=t.length;n<i;n++){const s=t[n];this.addLevel(s.object.clone(),s.distance,s.hysteresis)}return this.autoUpdate=e.autoUpdate,this}addLevel(e,t=0,n=0){t=Math.abs(t);const i=this.levels;let s;for(s=0;s<i.length&&!(t<i[s].distance);s++);return i.splice(s,0,{distance:t,hysteresis:n,object:e}),this.add(e),this}removeLevel(e){const t=this.levels;for(let n=0;n<t.length;n++)if(t[n].distance===e){const i=t.splice(n,1);return this.remove(i[0].object),!0}return!1}getCurrentLevel(){return this._currentLevel}getObjectForDistance(e){const t=this.levels;if(t.length>0){let n,i;for(n=1,i=t.length;n<i;n++){let s=t[n].distance;if(t[n].object.visible&&(s-=s*t[n].hysteresis),e<s)break}return t[n-1].object}return null}raycast(e,t){if(this.levels.length>0){Lc.setFromMatrixPosition(this.matrixWorld);const i=e.ray.origin.distanceTo(Lc);this.getObjectForDistance(i).raycast(e,t)}}update(e){const t=this.levels;if(t.length>1){Lc.setFromMatrixPosition(e.matrixWorld),y0.setFromMatrixPosition(this.matrixWorld);const n=Lc.distanceTo(y0)/e.zoom;t[0].object.visible=!0;let i,s;for(i=1,s=t.length;i<s;i++){let l=t[i].distance;if(t[i].object.visible&&(l-=l*t[i].hysteresis),n>=l)t[i-1].object.visible=!1,t[i].object.visible=!0;else break}for(this._currentLevel=i-1;i<s;i++)t[i].object.visible=!1}}toJSON(e){const t=super.toJSON(e);this.autoUpdate===!1&&(t.object.autoUpdate=!1),t.object.levels=[];const n=this.levels;for(let i=0,s=n.length;i<s;i++){const l=n[i];t.object.levels.push({object:l.object.uuid,distance:l.distance,hysteresis:l.hysteresis})}return t}}const x0=new L,S0=new At,M0=new At,KT=new L,E0=new ut,Dc=new L,cd=new yn,w0=new ut,ud=new Os;class B_ extends nn{constructor(e,t){super(e,t),this.isSkinnedMesh=!0,this.type="SkinnedMesh",this.bindMode=kd,this.bindMatrix=new ut,this.bindMatrixInverse=new ut,this.boundingBox=null,this.boundingSphere=null}computeBoundingBox(){const e=this.geometry;this.boundingBox===null&&(this.boundingBox=new _n),this.boundingBox.makeEmpty();const t=e.getAttribute("position");for(let n=0;n<t.count;n++)this.getVertexPosition(n,Dc),this.boundingBox.expandByPoint(Dc)}computeBoundingSphere(){const e=this.geometry;this.boundingSphere===null&&(this.boundingSphere=new yn),this.boundingSphere.makeEmpty();const t=e.getAttribute("position");for(let n=0;n<t.count;n++)this.getVertexPosition(n,Dc),this.boundingSphere.expandByPoint(Dc)}copy(e,t){return super.copy(e,t),this.bindMode=e.bindMode,this.bindMatrix.copy(e.bindMatrix),this.bindMatrixInverse.copy(e.bindMatrixInverse),this.skeleton=e.skeleton,e.boundingBox!==null&&(this.boundingBox=e.boundingBox.clone()),e.boundingSphere!==null&&(this.boundingSphere=e.boundingSphere.clone()),this}raycast(e,t){const n=this.material,i=this.matrixWorld;n!==void 0&&(this.boundingSphere===null&&this.computeBoundingSphere(),cd.copy(this.boundingSphere),cd.applyMatrix4(i),e.ray.intersectsSphere(cd)!==!1&&(w0.copy(i).invert(),ud.copy(e.ray).applyMatrix4(w0),!(this.boundingBox!==null&&ud.intersectsBox(this.boundingBox)===!1)&&this._computeIntersections(e,t,ud)))}getVertexPosition(e,t){return super.getVertexPosition(e,t),this.applyBoneTransform(e,t),t}bind(e,t){this.skeleton=e,t===void 0&&(this.updateMatrixWorld(!0),this.skeleton.calculateInverses(),t=this.matrixWorld),this.bindMatrix.copy(t),this.bindMatrixInverse.copy(t).invert()}pose(){this.skeleton.pose()}normalizeSkinWeights(){const e=new At,t=this.geometry.attributes.skinWeight;for(let n=0,i=t.count;n<i;n++){e.fromBufferAttribute(t,n);const s=1/e.manhattanLength();s!==1/0?e.multiplyScalar(s):e.set(1,0,0,0),t.setXYZW(n,e.x,e.y,e.z,e.w)}}updateMatrixWorld(e){super.updateMatrixWorld(e),this.bindMode===kd?this.bindMatrixInverse.copy(this.matrixWorld).invert():this.bindMode===r_?this.bindMatrixInverse.copy(this.bindMatrix).invert():console.warn("THREE.SkinnedMesh: Unrecognized bindMode: "+this.bindMode)}applyBoneTransform(e,t){const n=this.skeleton,i=this.geometry;S0.fromBufferAttribute(i.attributes.skinIndex,e),M0.fromBufferAttribute(i.attributes.skinWeight,e),x0.copy(t).applyMatrix4(this.bindMatrix),t.set(0,0,0);for(let s=0;s<4;s++){const l=M0.getComponent(s);if(l!==0){const c=S0.getComponent(s);E0.multiplyMatrices(n.bones[c].matrixWorld,n.boneInverses[c]),t.addScaledVector(KT.copy(x0).applyMatrix4(E0),l)}}return t.applyMatrix4(this.bindMatrixInverse)}}class wp extends Dt{constructor(){super(),this.isBone=!0,this.type="Bone"}}class Zi extends Kt{constructor(e=null,t=1,n=1,i,s,l,c,u,h=wn,f=wn,p,m){super(null,l,c,u,h,f,i,s,p,m),this.isDataTexture=!0,this.image={data:e,width:t,height:n},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}const T0=new ut,QT=new ut;class hh{constructor(e=[],t=[]){this.uuid=oi(),this.bones=e.slice(0),this.boneInverses=t,this.boneMatrices=null,this.boneTexture=null,this.init()}init(){const e=this.bones,t=this.boneInverses;if(this.boneMatrices=new Float32Array(e.length*16),t.length===0)this.calculateInverses();else if(e.length!==t.length){console.warn("THREE.Skeleton: Number of inverse bone matrices does not match amount of bones."),this.boneInverses=[];for(let n=0,i=this.bones.length;n<i;n++)this.boneInverses.push(new ut)}}calculateInverses(){this.boneInverses.length=0;for(let e=0,t=this.bones.length;e<t;e++){const n=new ut;this.bones[e]&&n.copy(this.bones[e].matrixWorld).invert(),this.boneInverses.push(n)}}pose(){for(let e=0,t=this.bones.length;e<t;e++){const n=this.bones[e];n&&n.matrixWorld.copy(this.boneInverses[e]).invert()}for(let e=0,t=this.bones.length;e<t;e++){const n=this.bones[e];n&&(n.parent&&n.parent.isBone?(n.matrix.copy(n.parent.matrixWorld).invert(),n.matrix.multiply(n.matrixWorld)):n.matrix.copy(n.matrixWorld),n.matrix.decompose(n.position,n.quaternion,n.scale))}}update(){const e=this.bones,t=this.boneInverses,n=this.boneMatrices,i=this.boneTexture;for(let s=0,l=e.length;s<l;s++){const c=e[s]?e[s].matrixWorld:QT;T0.multiplyMatrices(c,t[s]),T0.toArray(n,s*16)}i!==null&&(i.needsUpdate=!0)}clone(){return new hh(this.bones,this.boneInverses)}computeBoneTexture(){let e=Math.sqrt(this.bones.length*4);e=Math.ceil(e/4)*4,e=Math.max(e,4);const t=new Float32Array(e*e*4);t.set(this.boneMatrices);const n=new Zi(t,e,e,Dn,Kn);return n.needsUpdate=!0,this.boneMatrices=t,this.boneTexture=n,this}getBoneByName(e){for(let t=0,n=this.bones.length;t<n;t++){const i=this.bones[t];if(i.name===e)return i}}dispose(){this.boneTexture!==null&&(this.boneTexture.dispose(),this.boneTexture=null)}fromJSON(e,t){this.uuid=e.uuid;for(let n=0,i=e.bones.length;n<i;n++){const s=e.bones[n];let l=t[s];l===void 0&&(console.warn("THREE.Skeleton: No bone found with UUID:",s),l=new wp),this.bones.push(l),this.boneInverses.push(new ut().fromArray(e.boneInverses[n]))}return this.init(),this}toJSON(){const e={metadata:{version:4.6,type:"Skeleton",generator:"Skeleton.toJSON"},bones:[],boneInverses:[]};e.uuid=this.uuid;const t=this.bones,n=this.boneInverses;for(let i=0,s=t.length;i<s;i++){const l=t[i];e.bones.push(l.uuid);const c=n[i];e.boneInverses.push(c.toArray())}return e}}class Uo extends zt{constructor(e,t,n,i=1){super(e,t,n),this.isInstancedBufferAttribute=!0,this.meshPerAttribute=i}copy(e){return super.copy(e),this.meshPerAttribute=e.meshPerAttribute,this}toJSON(){const e=super.toJSON();return e.meshPerAttribute=this.meshPerAttribute,e.isInstancedBufferAttribute=!0,e}}const yo=new ut,A0=new ut,Uc=[],b0=new _n,$T=new ut,da=new nn,pa=new yn;class z_ extends nn{constructor(e,t,n){super(e,t),this.isInstancedMesh=!0,this.instanceMatrix=new Uo(new Float32Array(n*16),16),this.instanceColor=null,this.morphTexture=null,this.count=n,this.boundingBox=null,this.boundingSphere=null;for(let i=0;i<n;i++)this.setMatrixAt(i,$T)}computeBoundingBox(){const e=this.geometry,t=this.count;this.boundingBox===null&&(this.boundingBox=new _n),e.boundingBox===null&&e.computeBoundingBox(),this.boundingBox.makeEmpty();for(let n=0;n<t;n++)this.getMatrixAt(n,yo),b0.copy(e.boundingBox).applyMatrix4(yo),this.boundingBox.union(b0)}computeBoundingSphere(){const e=this.geometry,t=this.count;this.boundingSphere===null&&(this.boundingSphere=new yn),e.boundingSphere===null&&e.computeBoundingSphere(),this.boundingSphere.makeEmpty();for(let n=0;n<t;n++)this.getMatrixAt(n,yo),pa.copy(e.boundingSphere).applyMatrix4(yo),this.boundingSphere.union(pa)}copy(e,t){return super.copy(e,t),this.instanceMatrix.copy(e.instanceMatrix),e.morphTexture!==null&&(this.morphTexture=e.morphTexture.clone()),e.instanceColor!==null&&(this.instanceColor=e.instanceColor.clone()),this.count=e.count,e.boundingBox!==null&&(this.boundingBox=e.boundingBox.clone()),e.boundingSphere!==null&&(this.boundingSphere=e.boundingSphere.clone()),this}getColorAt(e,t){t.fromArray(this.instanceColor.array,e*3)}getMatrixAt(e,t){t.fromArray(this.instanceMatrix.array,e*16)}getMorphAt(e,t){const n=t.morphTargetInfluences,i=this.morphTexture.source.data.data,s=n.length+1,l=e*s+1;for(let c=0;c<n.length;c++)n[c]=i[l+c]}raycast(e,t){const n=this.matrixWorld,i=this.count;if(da.geometry=this.geometry,da.material=this.material,da.material!==void 0&&(this.boundingSphere===null&&this.computeBoundingSphere(),pa.copy(this.boundingSphere),pa.applyMatrix4(n),e.ray.intersectsSphere(pa)!==!1))for(let s=0;s<i;s++){this.getMatrixAt(s,yo),A0.multiplyMatrices(n,yo),da.matrixWorld=A0,da.raycast(e,Uc);for(let l=0,c=Uc.length;l<c;l++){const u=Uc[l];u.instanceId=s,u.object=this,t.push(u)}Uc.length=0}}setColorAt(e,t){this.instanceColor===null&&(this.instanceColor=new Uo(new Float32Array(this.instanceMatrix.count*3).fill(1),3)),t.toArray(this.instanceColor.array,e*3)}setMatrixAt(e,t){t.toArray(this.instanceMatrix.array,e*16)}setMorphAt(e,t){const n=t.morphTargetInfluences,i=n.length+1;this.morphTexture===null&&(this.morphTexture=new Zi(new Float32Array(i*this.count),i,this.count,nh,Kn));const s=this.morphTexture.source.data.data;let l=0;for(let h=0;h<n.length;h++)l+=n[h];const c=this.geometry.morphTargetsRelative?1:1-l,u=i*e;s[u]=c,s.set(n,u+1)}updateMorphTargets(){}dispose(){return this.dispatchEvent({type:"dispose"}),this.morphTexture!==null&&(this.morphTexture.dispose(),this.morphTexture=null),this}}function hd(r,e){return r-e}function eA(r,e){return r.z-e.z}function tA(r,e){return e.z-r.z}class nA{constructor(){this.index=0,this.pool=[],this.list=[]}push(e,t,n,i){const s=this.pool,l=this.list;this.index>=s.length&&s.push({start:-1,count:-1,z:-1,index:-1});const c=s[this.index];l.push(c),this.index++,c.start=e,c.count=t,c.z=n,c.index=i}reset(){this.list.length=0,this.index=0}}const qn=new ut,iA=new Be(1,1,1),fd=new nl,Nc=new _n,cs=new yn,ma=new L,C0=new L,rA=new L,dd=new nA,Ln=new nn,Oc=[];function sA(r,e,t=0){const n=e.itemSize;if(r.isInterleavedBufferAttribute||r.array.constructor!==e.array.constructor){const i=r.count;for(let s=0;s<i;s++)for(let l=0;l<n;l++)e.setComponent(s+t,l,r.getComponent(s,l))}else e.array.set(r.array,t*n);e.needsUpdate=!0}function us(r,e){if(r.constructor!==e.constructor){const t=Math.min(r.length,e.length);for(let n=0;n<t;n++)e[n]=r[n]}else{const t=Math.min(r.length,e.length);e.set(new r.constructor(r.buffer,0,t))}}class k_ extends nn{get maxInstanceCount(){return this._maxInstanceCount}get instanceCount(){return this._instanceInfo.length-this._availableInstanceIds.length}get unusedVertexCount(){return this._maxVertexCount-this._nextVertexStart}get unusedIndexCount(){return this._maxIndexCount-this._nextIndexStart}constructor(e,t,n=t*2,i){super(new xt,i),this.isBatchedMesh=!0,this.perObjectFrustumCulled=!0,this.sortObjects=!0,this.boundingBox=null,this.boundingSphere=null,this.customSort=null,this._instanceInfo=[],this._geometryInfo=[],this._availableInstanceIds=[],this._availableGeometryIds=[],this._nextIndexStart=0,this._nextVertexStart=0,this._geometryCount=0,this._visibilityChanged=!0,this._geometryInitialized=!1,this._maxInstanceCount=e,this._maxVertexCount=t,this._maxIndexCount=n,this._multiDrawCounts=new Int32Array(e),this._multiDrawStarts=new Int32Array(e),this._multiDrawCount=0,this._multiDrawInstances=null,this._matricesTexture=null,this._indirectTexture=null,this._colorsTexture=null,this._initMatricesTexture(),this._initIndirectTexture()}_initMatricesTexture(){let e=Math.sqrt(this._maxInstanceCount*4);e=Math.ceil(e/4)*4,e=Math.max(e,4);const t=new Float32Array(e*e*4),n=new Zi(t,e,e,Dn,Kn);this._matricesTexture=n}_initIndirectTexture(){let e=Math.sqrt(this._maxInstanceCount);e=Math.ceil(e);const t=new Uint32Array(e*e),n=new Zi(t,e,e,Qa,yr);this._indirectTexture=n}_initColorsTexture(){let e=Math.sqrt(this._maxInstanceCount);e=Math.ceil(e);const t=new Float32Array(e*e*4).fill(1),n=new Zi(t,e,e,Dn,Kn);n.colorSpace=Pt.workingColorSpace,this._colorsTexture=n}_initializeGeometry(e){const t=this.geometry,n=this._maxVertexCount,i=this._maxIndexCount;if(this._geometryInitialized===!1){for(const s in e.attributes){const l=e.getAttribute(s),{array:c,itemSize:u,normalized:h}=l,f=new c.constructor(n*u),p=new zt(f,u,h);t.setAttribute(s,p)}if(e.getIndex()!==null){const s=n>65535?new Uint32Array(i):new Uint16Array(i);t.setIndex(new zt(s,1))}this._geometryInitialized=!0}}_validateGeometry(e){const t=this.geometry;if(!!e.getIndex()!=!!t.getIndex())throw new Error('BatchedMesh: All geometries must consistently have "index".');for(const n in t.attributes){if(!e.hasAttribute(n))throw new Error(`BatchedMesh: Added geometry missing "${n}". All geometries must have consistent attributes.`);const i=e.getAttribute(n),s=t.getAttribute(n);if(i.itemSize!==s.itemSize||i.normalized!==s.normalized)throw new Error("BatchedMesh: All attributes must have a consistent itemSize and normalized value.")}}setCustomSort(e){return this.customSort=e,this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new _n);const e=this.boundingBox,t=this._instanceInfo;e.makeEmpty();for(let n=0,i=t.length;n<i;n++){if(t[n].active===!1)continue;const s=t[n].geometryIndex;this.getMatrixAt(n,qn),this.getBoundingBoxAt(s,Nc).applyMatrix4(qn),e.union(Nc)}}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new yn);const e=this.boundingSphere,t=this._instanceInfo;e.makeEmpty();for(let n=0,i=t.length;n<i;n++){if(t[n].active===!1)continue;const s=t[n].geometryIndex;this.getMatrixAt(n,qn),this.getBoundingSphereAt(s,cs).applyMatrix4(qn),e.union(cs)}}addInstance(e){if(this._instanceInfo.length>=this.maxInstanceCount&&this._availableInstanceIds.length===0)throw new Error("BatchedMesh: Maximum item count reached.");const n={visible:!0,active:!0,geometryIndex:e};let i=null;this._availableInstanceIds.length>0?(this._availableInstanceIds.sort(hd),i=this._availableInstanceIds.shift(),this._instanceInfo[i]=n):(i=this._instanceInfo.length,this._instanceInfo.push(n));const s=this._matricesTexture;qn.identity().toArray(s.image.data,i*16),s.needsUpdate=!0;const l=this._colorsTexture;return l&&(iA.toArray(l.image.data,i*4),l.needsUpdate=!0),this._visibilityChanged=!0,i}addGeometry(e,t=-1,n=-1){this._initializeGeometry(e),this._validateGeometry(e);const i={vertexStart:-1,vertexCount:-1,reservedVertexCount:-1,indexStart:-1,indexCount:-1,reservedIndexCount:-1,start:-1,count:-1,boundingBox:null,boundingSphere:null,active:!0},s=this._geometryInfo;i.vertexStart=this._nextVertexStart,i.reservedVertexCount=t===-1?e.getAttribute("position").count:t;const l=e.getIndex();if(l!==null&&(i.indexStart=this._nextIndexStart,i.reservedIndexCount=n===-1?l.count:n),i.indexStart!==-1&&i.indexStart+i.reservedIndexCount>this._maxIndexCount||i.vertexStart+i.reservedVertexCount>this._maxVertexCount)throw new Error("BatchedMesh: Reserved space request exceeds the maximum buffer size.");let u;return this._availableGeometryIds.length>0?(this._availableGeometryIds.sort(hd),u=this._availableGeometryIds.shift(),s[u]=i):(u=this._geometryCount,this._geometryCount++,s.push(i)),this.setGeometryAt(u,e),this._nextIndexStart=i.indexStart+i.reservedIndexCount,this._nextVertexStart=i.vertexStart+i.reservedVertexCount,u}setGeometryAt(e,t){if(e>=this._geometryCount)throw new Error("BatchedMesh: Maximum geometry count reached.");this._validateGeometry(t);const n=this.geometry,i=n.getIndex()!==null,s=n.getIndex(),l=t.getIndex(),c=this._geometryInfo[e];if(i&&l.count>c.reservedIndexCount||t.attributes.position.count>c.reservedVertexCount)throw new Error("BatchedMesh: Reserved space not large enough for provided geometry.");const u=c.vertexStart,h=c.reservedVertexCount;c.vertexCount=t.getAttribute("position").count;for(const f in n.attributes){const p=t.getAttribute(f),m=n.getAttribute(f);sA(p,m,u);const g=p.itemSize;for(let y=p.count,M=h;y<M;y++){const x=u+y;for(let _=0;_<g;_++)m.setComponent(x,_,0)}m.needsUpdate=!0,m.addUpdateRange(u*g,h*g)}if(i){const f=c.indexStart,p=c.reservedIndexCount;c.indexCount=t.getIndex().count;for(let m=0;m<l.count;m++)s.setX(f+m,u+l.getX(m));for(let m=l.count,g=p;m<g;m++)s.setX(f+m,u);s.needsUpdate=!0,s.addUpdateRange(f,c.reservedIndexCount)}return c.start=i?c.indexStart:c.vertexStart,c.count=i?c.indexCount:c.vertexCount,c.boundingBox=null,t.boundingBox!==null&&(c.boundingBox=t.boundingBox.clone()),c.boundingSphere=null,t.boundingSphere!==null&&(c.boundingSphere=t.boundingSphere.clone()),this._visibilityChanged=!0,e}deleteGeometry(e){const t=this._geometryInfo;if(e>=t.length||t[e].active===!1)return this;const n=this._instanceInfo;for(let i=0,s=n.length;i<s;i++)n[i].geometryIndex===e&&this.deleteInstance(i);return t[e].active=!1,this._availableGeometryIds.push(e),this._visibilityChanged=!0,this}deleteInstance(e){const t=this._instanceInfo;return e>=t.length||t[e].active===!1?this:(t[e].active=!1,this._availableInstanceIds.push(e),this._visibilityChanged=!0,this)}optimize(){let e=0,t=0;const n=this._geometryInfo,i=n.map((l,c)=>c).sort((l,c)=>n[l].vertexStart-n[c].vertexStart),s=this.geometry;for(let l=0,c=n.length;l<c;l++){const u=i[l],h=n[u];if(h.active!==!1){if(s.index!==null){if(h.indexStart!==t){const{indexStart:f,vertexStart:p,reservedIndexCount:m}=h,g=s.index,y=g.array,M=e-p;for(let x=f;x<f+m;x++)y[x]=y[x]+M;g.array.copyWithin(t,f,f+m),g.addUpdateRange(t,m),h.indexStart=t}t+=h.reservedIndexCount}if(h.vertexStart!==e){const{vertexStart:f,reservedVertexCount:p}=h,m=s.attributes;for(const g in m){const y=m[g],{array:M,itemSize:x}=y;M.copyWithin(e*x,f*x,(f+p)*x),y.addUpdateRange(e*x,p*x)}h.vertexStart=e}e+=h.reservedVertexCount,h.start=s.index?h.indexStart:h.vertexStart,this._nextIndexStart=s.index?h.indexStart+h.reservedIndexCount:0,this._nextVertexStart=h.vertexStart+h.reservedVertexCount}}return this}getBoundingBoxAt(e,t){if(e>=this._geometryCount)return null;const n=this.geometry,i=this._geometryInfo[e];if(i.boundingBox===null){const s=new _n,l=n.index,c=n.attributes.position;for(let u=i.start,h=i.start+i.count;u<h;u++){let f=u;l&&(f=l.getX(f)),s.expandByPoint(ma.fromBufferAttribute(c,f))}i.boundingBox=s}return t.copy(i.boundingBox),t}getBoundingSphereAt(e,t){if(e>=this._geometryCount)return null;const n=this.geometry,i=this._geometryInfo[e];if(i.boundingSphere===null){const s=new yn;this.getBoundingBoxAt(e,Nc),Nc.getCenter(s.center);const l=n.index,c=n.attributes.position;let u=0;for(let h=i.start,f=i.start+i.count;h<f;h++){let p=h;l&&(p=l.getX(p)),ma.fromBufferAttribute(c,p),u=Math.max(u,s.center.distanceToSquared(ma))}s.radius=Math.sqrt(u),i.boundingSphere=s}return t.copy(i.boundingSphere),t}setMatrixAt(e,t){const n=this._instanceInfo,i=this._matricesTexture,s=this._matricesTexture.image.data;return e>=n.length||n[e].active===!1?this:(t.toArray(s,e*16),i.needsUpdate=!0,this)}getMatrixAt(e,t){const n=this._instanceInfo,i=this._matricesTexture.image.data;return e>=n.length||n[e].active===!1?null:t.fromArray(i,e*16)}setColorAt(e,t){this._colorsTexture===null&&this._initColorsTexture();const n=this._colorsTexture,i=this._colorsTexture.image.data,s=this._instanceInfo;return e>=s.length||s[e].active===!1?this:(t.toArray(i,e*4),n.needsUpdate=!0,this)}getColorAt(e,t){const n=this._colorsTexture.image.data,i=this._instanceInfo;return e>=i.length||i[e].active===!1?null:t.fromArray(n,e*4)}setVisibleAt(e,t){const n=this._instanceInfo;return e>=n.length||n[e].active===!1||n[e].visible===t?this:(n[e].visible=t,this._visibilityChanged=!0,this)}getVisibleAt(e){const t=this._instanceInfo;return e>=t.length||t[e].active===!1?!1:t[e].visible}setGeometryIdAt(e,t){const n=this._instanceInfo,i=this._geometryInfo;return e>=n.length||n[e].active===!1||t>=i.length||i[t].active===!1?null:(n[e].geometryIndex=t,this)}getGeometryIdAt(e){const t=this._instanceInfo;return e>=t.length||t[e].active===!1?-1:t[e].geometryIndex}getGeometryRangeAt(e,t={}){if(e<0||e>=this._geometryCount)return null;const n=this._geometryInfo[e];return t.vertexStart=n.vertexStart,t.vertexCount=n.vertexCount,t.reservedVertexCount=n.reservedVertexCount,t.indexStart=n.indexStart,t.indexCount=n.indexCount,t.reservedIndexCount=n.reservedIndexCount,t.start=n.start,t.count=n.count,t}setInstanceCount(e){const t=this._availableInstanceIds,n=this._instanceInfo;for(t.sort(hd);t[t.length-1]===n.length;)n.pop(),t.pop();if(e<n.length)throw new Error(`BatchedMesh: Instance ids outside the range ${e} are being used. Cannot shrink instance count.`);const i=new Int32Array(e),s=new Int32Array(e);us(this._multiDrawCounts,i),us(this._multiDrawStarts,s),this._multiDrawCounts=i,this._multiDrawStarts=s,this._maxInstanceCount=e;const l=this._indirectTexture,c=this._matricesTexture,u=this._colorsTexture;l.dispose(),this._initIndirectTexture(),us(l.image.data,this._indirectTexture.image.data),c.dispose(),this._initMatricesTexture(),us(c.image.data,this._matricesTexture.image.data),u&&(u.dispose(),this._initColorsTexture(),us(u.image.data,this._colorsTexture.image.data))}setGeometrySize(e,t){const n=[...this._geometryInfo].filter(c=>c.active);if(Math.max(...n.map(c=>c.vertexStart+c.reservedVertexCount))>e)throw new Error(`BatchedMesh: Geometry vertex values are being used outside the range ${t}. Cannot shrink further.`);if(this.geometry.index&&Math.max(...n.map(u=>u.indexStart+u.reservedIndexCount))>t)throw new Error(`BatchedMesh: Geometry index values are being used outside the range ${t}. Cannot shrink further.`);const s=this.geometry;s.dispose(),this._maxVertexCount=e,this._maxIndexCount=t,this._geometryInitialized&&(this._geometryInitialized=!1,this.geometry=new xt,this._initializeGeometry(s));const l=this.geometry;s.index&&us(s.index.array,l.index.array);for(const c in s.attributes)us(s.attributes[c].array,l.attributes[c].array)}raycast(e,t){const n=this._instanceInfo,i=this._geometryInfo,s=this.matrixWorld,l=this.geometry;Ln.material=this.material,Ln.geometry.index=l.index,Ln.geometry.attributes=l.attributes,Ln.geometry.boundingBox===null&&(Ln.geometry.boundingBox=new _n),Ln.geometry.boundingSphere===null&&(Ln.geometry.boundingSphere=new yn);for(let c=0,u=n.length;c<u;c++){if(!n[c].visible||!n[c].active)continue;const h=n[c].geometryIndex,f=i[h];Ln.geometry.setDrawRange(f.start,f.count),this.getMatrixAt(c,Ln.matrixWorld).premultiply(s),this.getBoundingBoxAt(h,Ln.geometry.boundingBox),this.getBoundingSphereAt(h,Ln.geometry.boundingSphere),Ln.raycast(e,Oc);for(let p=0,m=Oc.length;p<m;p++){const g=Oc[p];g.object=this,g.batchId=c,t.push(g)}Oc.length=0}Ln.material=null,Ln.geometry.index=null,Ln.geometry.attributes={},Ln.geometry.setDrawRange(0,1/0)}copy(e){return super.copy(e),this.geometry=e.geometry.clone(),this.perObjectFrustumCulled=e.perObjectFrustumCulled,this.sortObjects=e.sortObjects,this.boundingBox=e.boundingBox!==null?e.boundingBox.clone():null,this.boundingSphere=e.boundingSphere!==null?e.boundingSphere.clone():null,this._geometryInfo=e._geometryInfo.map(t=>({...t,boundingBox:t.boundingBox!==null?t.boundingBox.clone():null,boundingSphere:t.boundingSphere!==null?t.boundingSphere.clone():null})),this._instanceInfo=e._instanceInfo.map(t=>({...t})),this._maxInstanceCount=e._maxInstanceCount,this._maxVertexCount=e._maxVertexCount,this._maxIndexCount=e._maxIndexCount,this._geometryInitialized=e._geometryInitialized,this._geometryCount=e._geometryCount,this._multiDrawCounts=e._multiDrawCounts.slice(),this._multiDrawStarts=e._multiDrawStarts.slice(),this._matricesTexture=e._matricesTexture.clone(),this._matricesTexture.image.data=this._matricesTexture.image.data.slice(),this._colorsTexture!==null&&(this._colorsTexture=e._colorsTexture.clone(),this._colorsTexture.image.data=this._colorsTexture.image.data.slice()),this}dispose(){return this.geometry.dispose(),this._matricesTexture.dispose(),this._matricesTexture=null,this._indirectTexture.dispose(),this._indirectTexture=null,this._colorsTexture!==null&&(this._colorsTexture.dispose(),this._colorsTexture=null),this}onBeforeRender(e,t,n,i,s){if(!this._visibilityChanged&&!this.perObjectFrustumCulled&&!this.sortObjects)return;const l=i.getIndex(),c=l===null?1:l.array.BYTES_PER_ELEMENT,u=this._instanceInfo,h=this._multiDrawStarts,f=this._multiDrawCounts,p=this._geometryInfo,m=this.perObjectFrustumCulled,g=this._indirectTexture,y=g.image.data;m&&(qn.multiplyMatrices(n.projectionMatrix,n.matrixWorldInverse).multiply(this.matrixWorld),fd.setFromProjectionMatrix(qn,e.coordinateSystem));let M=0;if(this.sortObjects){qn.copy(this.matrixWorld).invert(),ma.setFromMatrixPosition(n.matrixWorld).applyMatrix4(qn),C0.set(0,0,-1).transformDirection(n.matrixWorld).transformDirection(qn);for(let w=0,E=u.length;w<E;w++)if(u[w].visible&&u[w].active){const T=u[w].geometryIndex;this.getMatrixAt(w,qn),this.getBoundingSphereAt(T,cs).applyMatrix4(qn);let U=!1;if(m&&(U=!fd.intersectsSphere(cs)),!U){const P=p[T],D=rA.subVectors(cs.center,ma).dot(C0);dd.push(P.start,P.count,D,w)}}const x=dd.list,_=this.customSort;_===null?x.sort(s.transparent?tA:eA):_.call(this,x,n);for(let w=0,E=x.length;w<E;w++){const T=x[w];h[M]=T.start*c,f[M]=T.count,y[M]=T.index,M++}dd.reset()}else for(let x=0,_=u.length;x<_;x++)if(u[x].visible&&u[x].active){const w=u[x].geometryIndex;let E=!1;if(m&&(this.getMatrixAt(x,qn),this.getBoundingSphereAt(w,cs).applyMatrix4(qn),E=!fd.intersectsSphere(cs)),!E){const T=p[w];h[M]=T.start*c,f[M]=T.count,y[M]=x,M++}}g.needsUpdate=!0,this._multiDrawCount=M,this._visibilityChanged=!1}onBeforeShadow(e,t,n,i,s,l){this.onBeforeRender(e,null,i,s,l)}}class Gn extends Nn{static get type(){return"LineBasicMaterial"}constructor(e){super(),this.isLineBasicMaterial=!0,this.color=new Be(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Yu=new L,qu=new L,R0=new ut,ga=new Os,Fc=new yn,pd=new L,P0=new L;let Vr=class extends Dt{constructor(e=new xt,t=new Gn){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,n=[0];for(let i=1,s=t.count;i<s;i++)Yu.fromBufferAttribute(t,i-1),qu.fromBufferAttribute(t,i),n[i]=n[i-1],n[i]+=Yu.distanceTo(qu);e.setAttribute("lineDistance",new Ye(n,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const n=this.geometry,i=this.matrixWorld,s=e.params.Line.threshold,l=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),Fc.copy(n.boundingSphere),Fc.applyMatrix4(i),Fc.radius+=s,e.ray.intersectsSphere(Fc)===!1)return;R0.copy(i).invert(),ga.copy(e.ray).applyMatrix4(R0);const c=s/((this.scale.x+this.scale.y+this.scale.z)/3),u=c*c,h=this.isLineSegments?2:1,f=n.index,m=n.attributes.position;if(f!==null){const g=Math.max(0,l.start),y=Math.min(f.count,l.start+l.count);for(let M=g,x=y-1;M<x;M+=h){const _=f.getX(M),w=f.getX(M+1),E=Bc(this,e,ga,u,_,w);E&&t.push(E)}if(this.isLineLoop){const M=f.getX(y-1),x=f.getX(g),_=Bc(this,e,ga,u,M,x);_&&t.push(_)}}else{const g=Math.max(0,l.start),y=Math.min(m.count,l.start+l.count);for(let M=g,x=y-1;M<x;M+=h){const _=Bc(this,e,ga,u,M,M+1);_&&t.push(_)}if(this.isLineLoop){const M=Bc(this,e,ga,u,y-1,g);M&&t.push(M)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,n=Object.keys(t);if(n.length>0){const i=t[n[0]];if(i!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,l=i.length;s<l;s++){const c=i[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}};function Bc(r,e,t,n,i,s){const l=r.geometry.attributes.position;if(Yu.fromBufferAttribute(l,i),qu.fromBufferAttribute(l,s),t.distanceSqToSegment(Yu,qu,pd,P0)>n)return;pd.applyMatrix4(r.matrixWorld);const u=e.ray.origin.distanceTo(pd);if(!(u<e.near||u>e.far))return{distance:u,point:P0.clone().applyMatrix4(r.matrixWorld),index:i,face:null,faceIndex:null,barycoord:null,object:r}}const I0=new L,L0=new L;class Ki extends Vr{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,n=[];for(let i=0,s=t.count;i<s;i+=2)I0.fromBufferAttribute(t,i),L0.fromBufferAttribute(t,i+1),n[i]=i===0?0:n[i-1],n[i+1]=n[i]+I0.distanceTo(L0);e.setAttribute("lineDistance",new Ye(n,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class H_ extends Vr{constructor(e,t){super(e,t),this.isLineLoop=!0,this.type="LineLoop"}}class Tp extends Nn{static get type(){return"PointsMaterial"}constructor(e){super(),this.isPointsMaterial=!0,this.color=new Be(16777215),this.map=null,this.alphaMap=null,this.size=1,this.sizeAttenuation=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.alphaMap=e.alphaMap,this.size=e.size,this.sizeAttenuation=e.sizeAttenuation,this.fog=e.fog,this}}const D0=new ut,Yd=new Os,zc=new yn,kc=new L;class V_ extends Dt{constructor(e=new xt,t=new Tp){super(),this.isPoints=!0,this.type="Points",this.geometry=e,this.material=t,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}raycast(e,t){const n=this.geometry,i=this.matrixWorld,s=e.params.Points.threshold,l=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),zc.copy(n.boundingSphere),zc.applyMatrix4(i),zc.radius+=s,e.ray.intersectsSphere(zc)===!1)return;D0.copy(i).invert(),Yd.copy(e.ray).applyMatrix4(D0);const c=s/((this.scale.x+this.scale.y+this.scale.z)/3),u=c*c,h=n.index,p=n.attributes.position;if(h!==null){const m=Math.max(0,l.start),g=Math.min(h.count,l.start+l.count);for(let y=m,M=g;y<M;y++){const x=h.getX(y);kc.fromBufferAttribute(p,x),U0(kc,x,u,i,e,t,this)}}else{const m=Math.max(0,l.start),g=Math.min(p.count,l.start+l.count);for(let y=m,M=g;y<M;y++)kc.fromBufferAttribute(p,y),U0(kc,y,u,i,e,t,this)}}updateMorphTargets(){const t=this.geometry.morphAttributes,n=Object.keys(t);if(n.length>0){const i=t[n[0]];if(i!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,l=i.length;s<l;s++){const c=i[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}}function U0(r,e,t,n,i,s,l){const c=Yd.distanceSqToPoint(r);if(c<t){const u=new L;Yd.closestPointToPoint(r,u),u.applyMatrix4(n);const h=i.ray.origin.distanceTo(u);if(h<i.near||h>i.far)return;s.push({distance:h,distanceToRay:Math.sqrt(c),point:u,index:e,face:null,faceIndex:null,barycoord:null,object:l})}}class oA extends Kt{constructor(e,t,n,i,s,l,c,u,h){super(e,t,n,i,s,l,c,u,h),this.isVideoTexture=!0,this.minFilter=l!==void 0?l:cn,this.magFilter=s!==void 0?s:cn,this.generateMipmaps=!1;const f=this;function p(){f.needsUpdate=!0,e.requestVideoFrameCallback(p)}"requestVideoFrameCallback"in e&&e.requestVideoFrameCallback(p)}clone(){return new this.constructor(this.image).copy(this)}update(){const e=this.image;"requestVideoFrameCallback"in e===!1&&e.readyState>=e.HAVE_CURRENT_DATA&&(this.needsUpdate=!0)}}class aA extends Kt{constructor(e,t){super({width:e,height:t}),this.isFramebufferTexture=!0,this.magFilter=wn,this.minFilter=wn,this.generateMipmaps=!1,this.needsUpdate=!0}}class fh extends Kt{constructor(e,t,n,i,s,l,c,u,h,f,p,m){super(null,l,c,u,h,f,i,s,p,m),this.isCompressedTexture=!0,this.image={width:t,height:n},this.mipmaps=e,this.flipY=!1,this.generateMipmaps=!1}}class lA extends fh{constructor(e,t,n,i,s,l){super(e,t,n,s,l),this.isCompressedArrayTexture=!0,this.image.depth=i,this.wrapR=vi,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class cA extends fh{constructor(e,t,n){super(void 0,e[0].width,e[0].height,t,n,_r),this.isCompressedCubeTexture=!0,this.isCubeTexture=!0,this.image=e}}class uA extends Kt{constructor(e,t,n,i,s,l,c,u,h){super(e,t,n,i,s,l,c,u,h),this.isCanvasTexture=!0,this.needsUpdate=!0}}class Ri{constructor(){this.type="Curve",this.arcLengthDivisions=200}getPoint(){return console.warn("THREE.Curve: .getPoint() not implemented."),null}getPointAt(e,t){const n=this.getUtoTmapping(e);return this.getPoint(n,t)}getPoints(e=5){const t=[];for(let n=0;n<=e;n++)t.push(this.getPoint(n/e));return t}getSpacedPoints(e=5){const t=[];for(let n=0;n<=e;n++)t.push(this.getPointAt(n/e));return t}getLength(){const e=this.getLengths();return e[e.length-1]}getLengths(e=this.arcLengthDivisions){if(this.cacheArcLengths&&this.cacheArcLengths.length===e+1&&!this.needsUpdate)return this.cacheArcLengths;this.needsUpdate=!1;const t=[];let n,i=this.getPoint(0),s=0;t.push(0);for(let l=1;l<=e;l++)n=this.getPoint(l/e),s+=n.distanceTo(i),t.push(s),i=n;return this.cacheArcLengths=t,t}updateArcLengths(){this.needsUpdate=!0,this.getLengths()}getUtoTmapping(e,t){const n=this.getLengths();let i=0;const s=n.length;let l;t?l=t:l=e*n[s-1];let c=0,u=s-1,h;for(;c<=u;)if(i=Math.floor(c+(u-c)/2),h=n[i]-l,h<0)c=i+1;else if(h>0)u=i-1;else{u=i;break}if(i=u,n[i]===l)return i/(s-1);const f=n[i],m=n[i+1]-f,g=(l-f)/m;return(i+g)/(s-1)}getTangent(e,t){let i=e-1e-4,s=e+1e-4;i<0&&(i=0),s>1&&(s=1);const l=this.getPoint(i),c=this.getPoint(s),u=t||(l.isVector2?new ae:new L);return u.copy(c).sub(l).normalize(),u}getTangentAt(e,t){const n=this.getUtoTmapping(e);return this.getTangent(n,t)}computeFrenetFrames(e,t){const n=new L,i=[],s=[],l=[],c=new L,u=new ut;for(let g=0;g<=e;g++){const y=g/e;i[g]=this.getTangentAt(y,new L)}s[0]=new L,l[0]=new L;let h=Number.MAX_VALUE;const f=Math.abs(i[0].x),p=Math.abs(i[0].y),m=Math.abs(i[0].z);f<=h&&(h=f,n.set(1,0,0)),p<=h&&(h=p,n.set(0,1,0)),m<=h&&n.set(0,0,1),c.crossVectors(i[0],n).normalize(),s[0].crossVectors(i[0],c),l[0].crossVectors(i[0],s[0]);for(let g=1;g<=e;g++){if(s[g]=s[g-1].clone(),l[g]=l[g-1].clone(),c.crossVectors(i[g-1],i[g]),c.length()>Number.EPSILON){c.normalize();const y=Math.acos(Jt(i[g-1].dot(i[g]),-1,1));s[g].applyMatrix4(u.makeRotationAxis(c,y))}l[g].crossVectors(i[g],s[g])}if(t===!0){let g=Math.acos(Jt(s[0].dot(s[e]),-1,1));g/=e,i[0].dot(c.crossVectors(s[0],s[e]))>0&&(g=-g);for(let y=1;y<=e;y++)s[y].applyMatrix4(u.makeRotationAxis(i[y],g*y)),l[y].crossVectors(i[y],s[y])}return{tangents:i,normals:s,binormals:l}}clone(){return new this.constructor().copy(this)}copy(e){return this.arcLengthDivisions=e.arcLengthDivisions,this}toJSON(){const e={metadata:{version:4.6,type:"Curve",generator:"Curve.toJSON"}};return e.arcLengthDivisions=this.arcLengthDivisions,e.type=this.type,e}fromJSON(e){return this.arcLengthDivisions=e.arcLengthDivisions,this}}class dh extends Ri{constructor(e=0,t=0,n=1,i=1,s=0,l=Math.PI*2,c=!1,u=0){super(),this.isEllipseCurve=!0,this.type="EllipseCurve",this.aX=e,this.aY=t,this.xRadius=n,this.yRadius=i,this.aStartAngle=s,this.aEndAngle=l,this.aClockwise=c,this.aRotation=u}getPoint(e,t=new ae){const n=t,i=Math.PI*2;let s=this.aEndAngle-this.aStartAngle;const l=Math.abs(s)<Number.EPSILON;for(;s<0;)s+=i;for(;s>i;)s-=i;s<Number.EPSILON&&(l?s=0:s=i),this.aClockwise===!0&&!l&&(s===i?s=-i:s=s-i);const c=this.aStartAngle+e*s;let u=this.aX+this.xRadius*Math.cos(c),h=this.aY+this.yRadius*Math.sin(c);if(this.aRotation!==0){const f=Math.cos(this.aRotation),p=Math.sin(this.aRotation),m=u-this.aX,g=h-this.aY;u=m*f-g*p+this.aX,h=m*p+g*f+this.aY}return n.set(u,h)}copy(e){return super.copy(e),this.aX=e.aX,this.aY=e.aY,this.xRadius=e.xRadius,this.yRadius=e.yRadius,this.aStartAngle=e.aStartAngle,this.aEndAngle=e.aEndAngle,this.aClockwise=e.aClockwise,this.aRotation=e.aRotation,this}toJSON(){const e=super.toJSON();return e.aX=this.aX,e.aY=this.aY,e.xRadius=this.xRadius,e.yRadius=this.yRadius,e.aStartAngle=this.aStartAngle,e.aEndAngle=this.aEndAngle,e.aClockwise=this.aClockwise,e.aRotation=this.aRotation,e}fromJSON(e){return super.fromJSON(e),this.aX=e.aX,this.aY=e.aY,this.xRadius=e.xRadius,this.yRadius=e.yRadius,this.aStartAngle=e.aStartAngle,this.aEndAngle=e.aEndAngle,this.aClockwise=e.aClockwise,this.aRotation=e.aRotation,this}}class G_ extends dh{constructor(e,t,n,i,s,l){super(e,t,n,n,i,s,l),this.isArcCurve=!0,this.type="ArcCurve"}}function Ap(){let r=0,e=0,t=0,n=0;function i(s,l,c,u){r=s,e=c,t=-3*s+3*l-2*c-u,n=2*s-2*l+c+u}return{initCatmullRom:function(s,l,c,u,h){i(l,c,h*(c-s),h*(u-l))},initNonuniformCatmullRom:function(s,l,c,u,h,f,p){let m=(l-s)/h-(c-s)/(h+f)+(c-l)/f,g=(c-l)/f-(u-l)/(f+p)+(u-c)/p;m*=f,g*=f,i(l,c,m,g)},calc:function(s){const l=s*s,c=l*s;return r+e*s+t*l+n*c}}}const Hc=new L,md=new Ap,gd=new Ap,vd=new Ap;class W_ extends Ri{constructor(e=[],t=!1,n="centripetal",i=.5){super(),this.isCatmullRomCurve3=!0,this.type="CatmullRomCurve3",this.points=e,this.closed=t,this.curveType=n,this.tension=i}getPoint(e,t=new L){const n=t,i=this.points,s=i.length,l=(s-(this.closed?0:1))*e;let c=Math.floor(l),u=l-c;this.closed?c+=c>0?0:(Math.floor(Math.abs(c)/s)+1)*s:u===0&&c===s-1&&(c=s-2,u=1);let h,f;this.closed||c>0?h=i[(c-1)%s]:(Hc.subVectors(i[0],i[1]).add(i[0]),h=Hc);const p=i[c%s],m=i[(c+1)%s];if(this.closed||c+2<s?f=i[(c+2)%s]:(Hc.subVectors(i[s-1],i[s-2]).add(i[s-1]),f=Hc),this.curveType==="centripetal"||this.curveType==="chordal"){const g=this.curveType==="chordal"?.5:.25;let y=Math.pow(h.distanceToSquared(p),g),M=Math.pow(p.distanceToSquared(m),g),x=Math.pow(m.distanceToSquared(f),g);M<1e-4&&(M=1),y<1e-4&&(y=M),x<1e-4&&(x=M),md.initNonuniformCatmullRom(h.x,p.x,m.x,f.x,y,M,x),gd.initNonuniformCatmullRom(h.y,p.y,m.y,f.y,y,M,x),vd.initNonuniformCatmullRom(h.z,p.z,m.z,f.z,y,M,x)}else this.curveType==="catmullrom"&&(md.initCatmullRom(h.x,p.x,m.x,f.x,this.tension),gd.initCatmullRom(h.y,p.y,m.y,f.y,this.tension),vd.initCatmullRom(h.z,p.z,m.z,f.z,this.tension));return n.set(md.calc(u),gd.calc(u),vd.calc(u)),n}copy(e){super.copy(e),this.points=[];for(let t=0,n=e.points.length;t<n;t++){const i=e.points[t];this.points.push(i.clone())}return this.closed=e.closed,this.curveType=e.curveType,this.tension=e.tension,this}toJSON(){const e=super.toJSON();e.points=[];for(let t=0,n=this.points.length;t<n;t++){const i=this.points[t];e.points.push(i.toArray())}return e.closed=this.closed,e.curveType=this.curveType,e.tension=this.tension,e}fromJSON(e){super.fromJSON(e),this.points=[];for(let t=0,n=e.points.length;t<n;t++){const i=e.points[t];this.points.push(new L().fromArray(i))}return this.closed=e.closed,this.curveType=e.curveType,this.tension=e.tension,this}}function N0(r,e,t,n,i){const s=(n-e)*.5,l=(i-t)*.5,c=r*r,u=r*c;return(2*t-2*n+s+l)*u+(-3*t+3*n-2*s-l)*c+s*r+t}function hA(r,e){const t=1-r;return t*t*e}function fA(r,e){return 2*(1-r)*r*e}function dA(r,e){return r*r*e}function Ia(r,e,t,n){return hA(r,e)+fA(r,t)+dA(r,n)}function pA(r,e){const t=1-r;return t*t*t*e}function mA(r,e){const t=1-r;return 3*t*t*r*e}function gA(r,e){return 3*(1-r)*r*r*e}function vA(r,e){return r*r*r*e}function La(r,e,t,n,i){return pA(r,e)+mA(r,t)+gA(r,n)+vA(r,i)}class bp extends Ri{constructor(e=new ae,t=new ae,n=new ae,i=new ae){super(),this.isCubicBezierCurve=!0,this.type="CubicBezierCurve",this.v0=e,this.v1=t,this.v2=n,this.v3=i}getPoint(e,t=new ae){const n=t,i=this.v0,s=this.v1,l=this.v2,c=this.v3;return n.set(La(e,i.x,s.x,l.x,c.x),La(e,i.y,s.y,l.y,c.y)),n}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this.v3.copy(e.v3),this}toJSON(){const e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e.v3=this.v3.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this.v3.fromArray(e.v3),this}}class X_ extends Ri{constructor(e=new L,t=new L,n=new L,i=new L){super(),this.isCubicBezierCurve3=!0,this.type="CubicBezierCurve3",this.v0=e,this.v1=t,this.v2=n,this.v3=i}getPoint(e,t=new L){const n=t,i=this.v0,s=this.v1,l=this.v2,c=this.v3;return n.set(La(e,i.x,s.x,l.x,c.x),La(e,i.y,s.y,l.y,c.y),La(e,i.z,s.z,l.z,c.z)),n}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this.v3.copy(e.v3),this}toJSON(){const e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e.v3=this.v3.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this.v3.fromArray(e.v3),this}}class Cp extends Ri{constructor(e=new ae,t=new ae){super(),this.isLineCurve=!0,this.type="LineCurve",this.v1=e,this.v2=t}getPoint(e,t=new ae){const n=t;return e===1?n.copy(this.v2):(n.copy(this.v2).sub(this.v1),n.multiplyScalar(e).add(this.v1)),n}getPointAt(e,t){return this.getPoint(e,t)}getTangent(e,t=new ae){return t.subVectors(this.v2,this.v1).normalize()}getTangentAt(e,t){return this.getTangent(e,t)}copy(e){return super.copy(e),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){const e=super.toJSON();return e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}}class Y_ extends Ri{constructor(e=new L,t=new L){super(),this.isLineCurve3=!0,this.type="LineCurve3",this.v1=e,this.v2=t}getPoint(e,t=new L){const n=t;return e===1?n.copy(this.v2):(n.copy(this.v2).sub(this.v1),n.multiplyScalar(e).add(this.v1)),n}getPointAt(e,t){return this.getPoint(e,t)}getTangent(e,t=new L){return t.subVectors(this.v2,this.v1).normalize()}getTangentAt(e,t){return this.getTangent(e,t)}copy(e){return super.copy(e),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){const e=super.toJSON();return e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}}class Rp extends Ri{constructor(e=new ae,t=new ae,n=new ae){super(),this.isQuadraticBezierCurve=!0,this.type="QuadraticBezierCurve",this.v0=e,this.v1=t,this.v2=n}getPoint(e,t=new ae){const n=t,i=this.v0,s=this.v1,l=this.v2;return n.set(Ia(e,i.x,s.x,l.x),Ia(e,i.y,s.y,l.y)),n}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){const e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}}class Pp extends Ri{constructor(e=new L,t=new L,n=new L){super(),this.isQuadraticBezierCurve3=!0,this.type="QuadraticBezierCurve3",this.v0=e,this.v1=t,this.v2=n}getPoint(e,t=new L){const n=t,i=this.v0,s=this.v1,l=this.v2;return n.set(Ia(e,i.x,s.x,l.x),Ia(e,i.y,s.y,l.y),Ia(e,i.z,s.z,l.z)),n}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){const e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}}class Ip extends Ri{constructor(e=[]){super(),this.isSplineCurve=!0,this.type="SplineCurve",this.points=e}getPoint(e,t=new ae){const n=t,i=this.points,s=(i.length-1)*e,l=Math.floor(s),c=s-l,u=i[l===0?l:l-1],h=i[l],f=i[l>i.length-2?i.length-1:l+1],p=i[l>i.length-3?i.length-1:l+2];return n.set(N0(c,u.x,h.x,f.x,p.x),N0(c,u.y,h.y,f.y,p.y)),n}copy(e){super.copy(e),this.points=[];for(let t=0,n=e.points.length;t<n;t++){const i=e.points[t];this.points.push(i.clone())}return this}toJSON(){const e=super.toJSON();e.points=[];for(let t=0,n=this.points.length;t<n;t++){const i=this.points[t];e.points.push(i.toArray())}return e}fromJSON(e){super.fromJSON(e),this.points=[];for(let t=0,n=e.points.length;t<n;t++){const i=e.points[t];this.points.push(new ae().fromArray(i))}return this}}var Zu=Object.freeze({__proto__:null,ArcCurve:G_,CatmullRomCurve3:W_,CubicBezierCurve:bp,CubicBezierCurve3:X_,EllipseCurve:dh,LineCurve:Cp,LineCurve3:Y_,QuadraticBezierCurve:Rp,QuadraticBezierCurve3:Pp,SplineCurve:Ip});class q_ extends Ri{constructor(){super(),this.type="CurvePath",this.curves=[],this.autoClose=!1}add(e){this.curves.push(e)}closePath(){const e=this.curves[0].getPoint(0),t=this.curves[this.curves.length-1].getPoint(1);if(!e.equals(t)){const n=e.isVector2===!0?"LineCurve":"LineCurve3";this.curves.push(new Zu[n](t,e))}return this}getPoint(e,t){const n=e*this.getLength(),i=this.getCurveLengths();let s=0;for(;s<i.length;){if(i[s]>=n){const l=i[s]-n,c=this.curves[s],u=c.getLength(),h=u===0?0:1-l/u;return c.getPointAt(h,t)}s++}return null}getLength(){const e=this.getCurveLengths();return e[e.length-1]}updateArcLengths(){this.needsUpdate=!0,this.cacheLengths=null,this.getCurveLengths()}getCurveLengths(){if(this.cacheLengths&&this.cacheLengths.length===this.curves.length)return this.cacheLengths;const e=[];let t=0;for(let n=0,i=this.curves.length;n<i;n++)t+=this.curves[n].getLength(),e.push(t);return this.cacheLengths=e,e}getSpacedPoints(e=40){const t=[];for(let n=0;n<=e;n++)t.push(this.getPoint(n/e));return this.autoClose&&t.push(t[0]),t}getPoints(e=12){const t=[];let n;for(let i=0,s=this.curves;i<s.length;i++){const l=s[i],c=l.isEllipseCurve?e*2:l.isLineCurve||l.isLineCurve3?1:l.isSplineCurve?e*l.points.length:e,u=l.getPoints(c);for(let h=0;h<u.length;h++){const f=u[h];n&&n.equals(f)||(t.push(f),n=f)}}return this.autoClose&&t.length>1&&!t[t.length-1].equals(t[0])&&t.push(t[0]),t}copy(e){super.copy(e),this.curves=[];for(let t=0,n=e.curves.length;t<n;t++){const i=e.curves[t];this.curves.push(i.clone())}return this.autoClose=e.autoClose,this}toJSON(){const e=super.toJSON();e.autoClose=this.autoClose,e.curves=[];for(let t=0,n=this.curves.length;t<n;t++){const i=this.curves[t];e.curves.push(i.toJSON())}return e}fromJSON(e){super.fromJSON(e),this.autoClose=e.autoClose,this.curves=[];for(let t=0,n=e.curves.length;t<n;t++){const i=e.curves[t];this.curves.push(new Zu[i.type]().fromJSON(i))}return this}}class Va extends q_{constructor(e){super(),this.type="Path",this.currentPoint=new ae,e&&this.setFromPoints(e)}setFromPoints(e){this.moveTo(e[0].x,e[0].y);for(let t=1,n=e.length;t<n;t++)this.lineTo(e[t].x,e[t].y);return this}moveTo(e,t){return this.currentPoint.set(e,t),this}lineTo(e,t){const n=new Cp(this.currentPoint.clone(),new ae(e,t));return this.curves.push(n),this.currentPoint.set(e,t),this}quadraticCurveTo(e,t,n,i){const s=new Rp(this.currentPoint.clone(),new ae(e,t),new ae(n,i));return this.curves.push(s),this.currentPoint.set(n,i),this}bezierCurveTo(e,t,n,i,s,l){const c=new bp(this.currentPoint.clone(),new ae(e,t),new ae(n,i),new ae(s,l));return this.curves.push(c),this.currentPoint.set(s,l),this}splineThru(e){const t=[this.currentPoint.clone()].concat(e),n=new Ip(t);return this.curves.push(n),this.currentPoint.copy(e[e.length-1]),this}arc(e,t,n,i,s,l){const c=this.currentPoint.x,u=this.currentPoint.y;return this.absarc(e+c,t+u,n,i,s,l),this}absarc(e,t,n,i,s,l){return this.absellipse(e,t,n,n,i,s,l),this}ellipse(e,t,n,i,s,l,c,u){const h=this.currentPoint.x,f=this.currentPoint.y;return this.absellipse(e+h,t+f,n,i,s,l,c,u),this}absellipse(e,t,n,i,s,l,c,u){const h=new dh(e,t,n,i,s,l,c,u);if(this.curves.length>0){const p=h.getPoint(0);p.equals(this.currentPoint)||this.lineTo(p.x,p.y)}this.curves.push(h);const f=h.getPoint(1);return this.currentPoint.copy(f),this}copy(e){return super.copy(e),this.currentPoint.copy(e.currentPoint),this}toJSON(){const e=super.toJSON();return e.currentPoint=this.currentPoint.toArray(),e}fromJSON(e){return super.fromJSON(e),this.currentPoint.fromArray(e.currentPoint),this}}class il extends xt{constructor(e=[new ae(0,-.5),new ae(.5,0),new ae(0,.5)],t=12,n=0,i=Math.PI*2){super(),this.type="LatheGeometry",this.parameters={points:e,segments:t,phiStart:n,phiLength:i},t=Math.floor(t),i=Jt(i,0,Math.PI*2);const s=[],l=[],c=[],u=[],h=[],f=1/t,p=new L,m=new ae,g=new L,y=new L,M=new L;let x=0,_=0;for(let w=0;w<=e.length-1;w++)switch(w){case 0:x=e[w+1].x-e[w].x,_=e[w+1].y-e[w].y,g.x=_*1,g.y=-x,g.z=_*0,M.copy(g),g.normalize(),u.push(g.x,g.y,g.z);break;case e.length-1:u.push(M.x,M.y,M.z);break;default:x=e[w+1].x-e[w].x,_=e[w+1].y-e[w].y,g.x=_*1,g.y=-x,g.z=_*0,y.copy(g),g.x+=M.x,g.y+=M.y,g.z+=M.z,g.normalize(),u.push(g.x,g.y,g.z),M.copy(y)}for(let w=0;w<=t;w++){const E=n+w*f*i,T=Math.sin(E),U=Math.cos(E);for(let P=0;P<=e.length-1;P++){p.x=e[P].x*T,p.y=e[P].y,p.z=e[P].x*U,l.push(p.x,p.y,p.z),m.x=w/t,m.y=P/(e.length-1),c.push(m.x,m.y);const D=u[3*P+0]*T,F=u[3*P+1],C=u[3*P+0]*U;h.push(D,F,C)}}for(let w=0;w<t;w++)for(let E=0;E<e.length-1;E++){const T=E+w*e.length,U=T,P=T+e.length,D=T+e.length+1,F=T+1;s.push(U,P,F),s.push(D,F,P)}this.setIndex(s),this.setAttribute("position",new Ye(l,3)),this.setAttribute("uv",new Ye(c,2)),this.setAttribute("normal",new Ye(h,3))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new il(e.points,e.segments,e.phiStart,e.phiLength)}}class ph extends il{constructor(e=1,t=1,n=4,i=8){const s=new Va;s.absarc(0,-t/2,e,Math.PI*1.5,0),s.absarc(0,t/2,e,0,Math.PI*.5),super(s.getPoints(n),i),this.type="CapsuleGeometry",this.parameters={radius:e,length:t,capSegments:n,radialSegments:i}}static fromJSON(e){return new ph(e.radius,e.length,e.capSegments,e.radialSegments)}}class mh extends xt{constructor(e=1,t=32,n=0,i=Math.PI*2){super(),this.type="CircleGeometry",this.parameters={radius:e,segments:t,thetaStart:n,thetaLength:i},t=Math.max(3,t);const s=[],l=[],c=[],u=[],h=new L,f=new ae;l.push(0,0,0),c.push(0,0,1),u.push(.5,.5);for(let p=0,m=3;p<=t;p++,m+=3){const g=n+p/t*i;h.x=e*Math.cos(g),h.y=e*Math.sin(g),l.push(h.x,h.y,h.z),c.push(0,0,1),f.x=(l[m]/e+1)/2,f.y=(l[m+1]/e+1)/2,u.push(f.x,f.y)}for(let p=1;p<=t;p++)s.push(p,p+1,0);this.setIndex(s),this.setAttribute("position",new Ye(l,3)),this.setAttribute("normal",new Ye(c,3)),this.setAttribute("uv",new Ye(u,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new mh(e.radius,e.segments,e.thetaStart,e.thetaLength)}}class ko extends xt{constructor(e=1,t=1,n=1,i=32,s=1,l=!1,c=0,u=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:n,radialSegments:i,heightSegments:s,openEnded:l,thetaStart:c,thetaLength:u};const h=this;i=Math.floor(i),s=Math.floor(s);const f=[],p=[],m=[],g=[];let y=0;const M=[],x=n/2;let _=0;w(),l===!1&&(e>0&&E(!0),t>0&&E(!1)),this.setIndex(f),this.setAttribute("position",new Ye(p,3)),this.setAttribute("normal",new Ye(m,3)),this.setAttribute("uv",new Ye(g,2));function w(){const T=new L,U=new L;let P=0;const D=(t-e)/n;for(let F=0;F<=s;F++){const C=[],b=F/s,N=b*(t-e)+e;for(let q=0;q<=i;q++){const Y=q/i,K=Y*u+c,le=Math.sin(K),$=Math.cos(K);U.x=N*le,U.y=-b*n+x,U.z=N*$,p.push(U.x,U.y,U.z),T.set(le,D,$).normalize(),m.push(T.x,T.y,T.z),g.push(Y,1-b),C.push(y++)}M.push(C)}for(let F=0;F<i;F++)for(let C=0;C<s;C++){const b=M[C][F],N=M[C+1][F],q=M[C+1][F+1],Y=M[C][F+1];(e>0||C!==0)&&(f.push(b,N,Y),P+=3),(t>0||C!==s-1)&&(f.push(N,q,Y),P+=3)}h.addGroup(_,P,0),_+=P}function E(T){const U=y,P=new ae,D=new L;let F=0;const C=T===!0?e:t,b=T===!0?1:-1;for(let q=1;q<=i;q++)p.push(0,x*b,0),m.push(0,b,0),g.push(.5,.5),y++;const N=y;for(let q=0;q<=i;q++){const K=q/i*u+c,le=Math.cos(K),$=Math.sin(K);D.x=C*$,D.y=x*b,D.z=C*le,p.push(D.x,D.y,D.z),m.push(0,b,0),P.x=le*.5+.5,P.y=$*.5*b+.5,g.push(P.x,P.y),y++}for(let q=0;q<i;q++){const Y=U+q,K=N+q;T===!0?f.push(K,K+1,Y):f.push(K+1,K,Y),F+=3}h.addGroup(_,F,T===!0?1:2),_+=F}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ko(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class gh extends ko{constructor(e=1,t=1,n=32,i=1,s=!1,l=0,c=Math.PI*2){super(0,e,t,n,i,s,l,c),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:n,heightSegments:i,openEnded:s,thetaStart:l,thetaLength:c}}static fromJSON(e){return new gh(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Xr extends xt{constructor(e=[],t=[],n=1,i=0){super(),this.type="PolyhedronGeometry",this.parameters={vertices:e,indices:t,radius:n,detail:i};const s=[],l=[];c(i),h(n),f(),this.setAttribute("position",new Ye(s,3)),this.setAttribute("normal",new Ye(s.slice(),3)),this.setAttribute("uv",new Ye(l,2)),i===0?this.computeVertexNormals():this.normalizeNormals();function c(w){const E=new L,T=new L,U=new L;for(let P=0;P<t.length;P+=3)g(t[P+0],E),g(t[P+1],T),g(t[P+2],U),u(E,T,U,w)}function u(w,E,T,U){const P=U+1,D=[];for(let F=0;F<=P;F++){D[F]=[];const C=w.clone().lerp(T,F/P),b=E.clone().lerp(T,F/P),N=P-F;for(let q=0;q<=N;q++)q===0&&F===P?D[F][q]=C:D[F][q]=C.clone().lerp(b,q/N)}for(let F=0;F<P;F++)for(let C=0;C<2*(P-F)-1;C++){const b=Math.floor(C/2);C%2===0?(m(D[F][b+1]),m(D[F+1][b]),m(D[F][b])):(m(D[F][b+1]),m(D[F+1][b+1]),m(D[F+1][b]))}}function h(w){const E=new L;for(let T=0;T<s.length;T+=3)E.x=s[T+0],E.y=s[T+1],E.z=s[T+2],E.normalize().multiplyScalar(w),s[T+0]=E.x,s[T+1]=E.y,s[T+2]=E.z}function f(){const w=new L;for(let E=0;E<s.length;E+=3){w.x=s[E+0],w.y=s[E+1],w.z=s[E+2];const T=x(w)/2/Math.PI+.5,U=_(w)/Math.PI+.5;l.push(T,1-U)}y(),p()}function p(){for(let w=0;w<l.length;w+=6){const E=l[w+0],T=l[w+2],U=l[w+4],P=Math.max(E,T,U),D=Math.min(E,T,U);P>.9&&D<.1&&(E<.2&&(l[w+0]+=1),T<.2&&(l[w+2]+=1),U<.2&&(l[w+4]+=1))}}function m(w){s.push(w.x,w.y,w.z)}function g(w,E){const T=w*3;E.x=e[T+0],E.y=e[T+1],E.z=e[T+2]}function y(){const w=new L,E=new L,T=new L,U=new L,P=new ae,D=new ae,F=new ae;for(let C=0,b=0;C<s.length;C+=9,b+=6){w.set(s[C+0],s[C+1],s[C+2]),E.set(s[C+3],s[C+4],s[C+5]),T.set(s[C+6],s[C+7],s[C+8]),P.set(l[b+0],l[b+1]),D.set(l[b+2],l[b+3]),F.set(l[b+4],l[b+5]),U.copy(w).add(E).add(T).divideScalar(3);const N=x(U);M(P,b+0,w,N),M(D,b+2,E,N),M(F,b+4,T,N)}}function M(w,E,T,U){U<0&&w.x===1&&(l[E]=w.x-1),T.x===0&&T.z===0&&(l[E]=U/2/Math.PI+.5)}function x(w){return Math.atan2(w.z,-w.x)}function _(w){return Math.atan2(-w.y,Math.sqrt(w.x*w.x+w.z*w.z))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Xr(e.vertices,e.indices,e.radius,e.details)}}class vh extends Xr{constructor(e=1,t=0){const n=(1+Math.sqrt(5))/2,i=1/n,s=[-1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,-1,-1,1,-1,1,1,1,-1,1,1,1,0,-i,-n,0,-i,n,0,i,-n,0,i,n,-i,-n,0,-i,n,0,i,-n,0,i,n,0,-n,0,-i,n,0,-i,-n,0,i,n,0,i],l=[3,11,7,3,7,15,3,15,13,7,19,17,7,17,6,7,6,15,17,4,8,17,8,10,17,10,6,8,0,16,8,16,2,8,2,10,0,12,1,0,1,18,0,18,16,6,10,2,6,2,13,6,13,15,2,16,18,2,18,3,2,3,13,18,1,9,18,9,11,18,11,3,4,14,12,4,12,0,4,0,8,11,9,5,11,5,19,11,19,7,19,5,14,19,14,4,19,4,17,1,12,14,1,14,5,1,5,9];super(s,l,e,t),this.type="DodecahedronGeometry",this.parameters={radius:e,detail:t}}static fromJSON(e){return new vh(e.radius,e.detail)}}const Vc=new L,Gc=new L,_d=new L,Wc=new Jn;class Z_ extends xt{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const i=Math.pow(10,4),s=Math.cos(bs*t),l=e.getIndex(),c=e.getAttribute("position"),u=l?l.count:c.count,h=[0,0,0],f=["a","b","c"],p=new Array(3),m={},g=[];for(let y=0;y<u;y+=3){l?(h[0]=l.getX(y),h[1]=l.getX(y+1),h[2]=l.getX(y+2)):(h[0]=y,h[1]=y+1,h[2]=y+2);const{a:M,b:x,c:_}=Wc;if(M.fromBufferAttribute(c,h[0]),x.fromBufferAttribute(c,h[1]),_.fromBufferAttribute(c,h[2]),Wc.getNormal(_d),p[0]=`${Math.round(M.x*i)},${Math.round(M.y*i)},${Math.round(M.z*i)}`,p[1]=`${Math.round(x.x*i)},${Math.round(x.y*i)},${Math.round(x.z*i)}`,p[2]=`${Math.round(_.x*i)},${Math.round(_.y*i)},${Math.round(_.z*i)}`,!(p[0]===p[1]||p[1]===p[2]||p[2]===p[0]))for(let w=0;w<3;w++){const E=(w+1)%3,T=p[w],U=p[E],P=Wc[f[w]],D=Wc[f[E]],F=`${T}_${U}`,C=`${U}_${T}`;C in m&&m[C]?(_d.dot(m[C].normal)<=s&&(g.push(P.x,P.y,P.z),g.push(D.x,D.y,D.z)),m[C]=null):F in m||(m[F]={index0:h[w],index1:h[E],normal:_d.clone()})}}for(const y in m)if(m[y]){const{index0:M,index1:x}=m[y];Vc.fromBufferAttribute(c,M),Gc.fromBufferAttribute(c,x),g.push(Vc.x,Vc.y,Vc.z),g.push(Gc.x,Gc.y,Gc.z)}this.setAttribute("position",new Ye(g,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class Rs extends Va{constructor(e){super(e),this.uuid=oi(),this.type="Shape",this.holes=[]}getPointsHoles(e){const t=[];for(let n=0,i=this.holes.length;n<i;n++)t[n]=this.holes[n].getPoints(e);return t}extractPoints(e){return{shape:this.getPoints(e),holes:this.getPointsHoles(e)}}copy(e){super.copy(e),this.holes=[];for(let t=0,n=e.holes.length;t<n;t++){const i=e.holes[t];this.holes.push(i.clone())}return this}toJSON(){const e=super.toJSON();e.uuid=this.uuid,e.holes=[];for(let t=0,n=this.holes.length;t<n;t++){const i=this.holes[t];e.holes.push(i.toJSON())}return e}fromJSON(e){super.fromJSON(e),this.uuid=e.uuid,this.holes=[];for(let t=0,n=e.holes.length;t<n;t++){const i=e.holes[t];this.holes.push(new Va().fromJSON(i))}return this}}const _A={triangulate:function(r,e,t=2){const n=e&&e.length,i=n?e[0]*t:r.length;let s=j_(r,0,i,t,!0);const l=[];if(!s||s.next===s.prev)return l;let c,u,h,f,p,m,g;if(n&&(s=EA(r,e,s,t)),r.length>80*t){c=h=r[0],u=f=r[1];for(let y=t;y<i;y+=t)p=r[y],m=r[y+1],p<c&&(c=p),m<u&&(u=m),p>h&&(h=p),m>f&&(f=m);g=Math.max(h-c,f-u),g=g!==0?32767/g:0}return Ga(s,l,t,c,u,g,0),l}};function j_(r,e,t,n,i){let s,l;if(i===UA(r,e,t,n)>0)for(s=e;s<t;s+=n)l=O0(s,r[s],r[s+1],l);else for(s=t-n;s>=e;s-=n)l=O0(s,r[s],r[s+1],l);return l&&_h(l,l.next)&&(Xa(l),l=l.next),l}function Us(r,e){if(!r)return r;e||(e=r);let t=r,n;do if(n=!1,!t.steiner&&(_h(t,t.next)||qt(t.prev,t,t.next)===0)){if(Xa(t),t=e=t.prev,t===t.next)break;n=!0}else t=t.next;while(n||t!==e);return e}function Ga(r,e,t,n,i,s,l){if(!r)return;!l&&s&&CA(r,n,i,s);let c=r,u,h;for(;r.prev!==r.next;){if(u=r.prev,h=r.next,s?xA(r,n,i,s):yA(r)){e.push(u.i/t|0),e.push(r.i/t|0),e.push(h.i/t|0),Xa(r),r=h.next,c=h.next;continue}if(r=h,r===c){l?l===1?(r=SA(Us(r),e,t),Ga(r,e,t,n,i,s,2)):l===2&&MA(r,e,t,n,i,s):Ga(Us(r),e,t,n,i,s,1);break}}}function yA(r){const e=r.prev,t=r,n=r.next;if(qt(e,t,n)>=0)return!1;const i=e.x,s=t.x,l=n.x,c=e.y,u=t.y,h=n.y,f=i<s?i<l?i:l:s<l?s:l,p=c<u?c<h?c:h:u<h?u:h,m=i>s?i>l?i:l:s>l?s:l,g=c>u?c>h?c:h:u>h?u:h;let y=n.next;for(;y!==e;){if(y.x>=f&&y.x<=m&&y.y>=p&&y.y<=g&&Co(i,c,s,u,l,h,y.x,y.y)&&qt(y.prev,y,y.next)>=0)return!1;y=y.next}return!0}function xA(r,e,t,n){const i=r.prev,s=r,l=r.next;if(qt(i,s,l)>=0)return!1;const c=i.x,u=s.x,h=l.x,f=i.y,p=s.y,m=l.y,g=c<u?c<h?c:h:u<h?u:h,y=f<p?f<m?f:m:p<m?p:m,M=c>u?c>h?c:h:u>h?u:h,x=f>p?f>m?f:m:p>m?p:m,_=qd(g,y,e,t,n),w=qd(M,x,e,t,n);let E=r.prevZ,T=r.nextZ;for(;E&&E.z>=_&&T&&T.z<=w;){if(E.x>=g&&E.x<=M&&E.y>=y&&E.y<=x&&E!==i&&E!==l&&Co(c,f,u,p,h,m,E.x,E.y)&&qt(E.prev,E,E.next)>=0||(E=E.prevZ,T.x>=g&&T.x<=M&&T.y>=y&&T.y<=x&&T!==i&&T!==l&&Co(c,f,u,p,h,m,T.x,T.y)&&qt(T.prev,T,T.next)>=0))return!1;T=T.nextZ}for(;E&&E.z>=_;){if(E.x>=g&&E.x<=M&&E.y>=y&&E.y<=x&&E!==i&&E!==l&&Co(c,f,u,p,h,m,E.x,E.y)&&qt(E.prev,E,E.next)>=0)return!1;E=E.prevZ}for(;T&&T.z<=w;){if(T.x>=g&&T.x<=M&&T.y>=y&&T.y<=x&&T!==i&&T!==l&&Co(c,f,u,p,h,m,T.x,T.y)&&qt(T.prev,T,T.next)>=0)return!1;T=T.nextZ}return!0}function SA(r,e,t){let n=r;do{const i=n.prev,s=n.next.next;!_h(i,s)&&J_(i,n,n.next,s)&&Wa(i,s)&&Wa(s,i)&&(e.push(i.i/t|0),e.push(n.i/t|0),e.push(s.i/t|0),Xa(n),Xa(n.next),n=r=s),n=n.next}while(n!==r);return Us(n)}function MA(r,e,t,n,i,s){let l=r;do{let c=l.next.next;for(;c!==l.prev;){if(l.i!==c.i&&IA(l,c)){let u=K_(l,c);l=Us(l,l.next),u=Us(u,u.next),Ga(l,e,t,n,i,s,0),Ga(u,e,t,n,i,s,0);return}c=c.next}l=l.next}while(l!==r)}function EA(r,e,t,n){const i=[];let s,l,c,u,h;for(s=0,l=e.length;s<l;s++)c=e[s]*n,u=s<l-1?e[s+1]*n:r.length,h=j_(r,c,u,n,!1),h===h.next&&(h.steiner=!0),i.push(PA(h));for(i.sort(wA),s=0;s<i.length;s++)t=TA(i[s],t);return t}function wA(r,e){return r.x-e.x}function TA(r,e){const t=AA(r,e);if(!t)return e;const n=K_(t,r);return Us(n,n.next),Us(t,t.next)}function AA(r,e){let t=e,n=-1/0,i;const s=r.x,l=r.y;do{if(l<=t.y&&l>=t.next.y&&t.next.y!==t.y){const m=t.x+(l-t.y)*(t.next.x-t.x)/(t.next.y-t.y);if(m<=s&&m>n&&(n=m,i=t.x<t.next.x?t:t.next,m===s))return i}t=t.next}while(t!==e);if(!i)return null;const c=i,u=i.x,h=i.y;let f=1/0,p;t=i;do s>=t.x&&t.x>=u&&s!==t.x&&Co(l<h?s:n,l,u,h,l<h?n:s,l,t.x,t.y)&&(p=Math.abs(l-t.y)/(s-t.x),Wa(t,r)&&(p<f||p===f&&(t.x>i.x||t.x===i.x&&bA(i,t)))&&(i=t,f=p)),t=t.next;while(t!==c);return i}function bA(r,e){return qt(r.prev,r,e.prev)<0&&qt(e.next,r,r.next)<0}function CA(r,e,t,n){let i=r;do i.z===0&&(i.z=qd(i.x,i.y,e,t,n)),i.prevZ=i.prev,i.nextZ=i.next,i=i.next;while(i!==r);i.prevZ.nextZ=null,i.prevZ=null,RA(i)}function RA(r){let e,t,n,i,s,l,c,u,h=1;do{for(t=r,r=null,s=null,l=0;t;){for(l++,n=t,c=0,e=0;e<h&&(c++,n=n.nextZ,!!n);e++);for(u=h;c>0||u>0&&n;)c!==0&&(u===0||!n||t.z<=n.z)?(i=t,t=t.nextZ,c--):(i=n,n=n.nextZ,u--),s?s.nextZ=i:r=i,i.prevZ=s,s=i;t=n}s.nextZ=null,h*=2}while(l>1);return r}function qd(r,e,t,n,i){return r=(r-t)*i|0,e=(e-n)*i|0,r=(r|r<<8)&16711935,r=(r|r<<4)&252645135,r=(r|r<<2)&858993459,r=(r|r<<1)&1431655765,e=(e|e<<8)&16711935,e=(e|e<<4)&252645135,e=(e|e<<2)&858993459,e=(e|e<<1)&1431655765,r|e<<1}function PA(r){let e=r,t=r;do(e.x<t.x||e.x===t.x&&e.y<t.y)&&(t=e),e=e.next;while(e!==r);return t}function Co(r,e,t,n,i,s,l,c){return(i-l)*(e-c)>=(r-l)*(s-c)&&(r-l)*(n-c)>=(t-l)*(e-c)&&(t-l)*(s-c)>=(i-l)*(n-c)}function IA(r,e){return r.next.i!==e.i&&r.prev.i!==e.i&&!LA(r,e)&&(Wa(r,e)&&Wa(e,r)&&DA(r,e)&&(qt(r.prev,r,e.prev)||qt(r,e.prev,e))||_h(r,e)&&qt(r.prev,r,r.next)>0&&qt(e.prev,e,e.next)>0)}function qt(r,e,t){return(e.y-r.y)*(t.x-e.x)-(e.x-r.x)*(t.y-e.y)}function _h(r,e){return r.x===e.x&&r.y===e.y}function J_(r,e,t,n){const i=Yc(qt(r,e,t)),s=Yc(qt(r,e,n)),l=Yc(qt(t,n,r)),c=Yc(qt(t,n,e));return!!(i!==s&&l!==c||i===0&&Xc(r,t,e)||s===0&&Xc(r,n,e)||l===0&&Xc(t,r,n)||c===0&&Xc(t,e,n))}function Xc(r,e,t){return e.x<=Math.max(r.x,t.x)&&e.x>=Math.min(r.x,t.x)&&e.y<=Math.max(r.y,t.y)&&e.y>=Math.min(r.y,t.y)}function Yc(r){return r>0?1:r<0?-1:0}function LA(r,e){let t=r;do{if(t.i!==r.i&&t.next.i!==r.i&&t.i!==e.i&&t.next.i!==e.i&&J_(t,t.next,r,e))return!0;t=t.next}while(t!==r);return!1}function Wa(r,e){return qt(r.prev,r,r.next)<0?qt(r,e,r.next)>=0&&qt(r,r.prev,e)>=0:qt(r,e,r.prev)<0||qt(r,r.next,e)<0}function DA(r,e){let t=r,n=!1;const i=(r.x+e.x)/2,s=(r.y+e.y)/2;do t.y>s!=t.next.y>s&&t.next.y!==t.y&&i<(t.next.x-t.x)*(s-t.y)/(t.next.y-t.y)+t.x&&(n=!n),t=t.next;while(t!==r);return n}function K_(r,e){const t=new Zd(r.i,r.x,r.y),n=new Zd(e.i,e.x,e.y),i=r.next,s=e.prev;return r.next=e,e.prev=r,t.next=i,i.prev=t,n.next=t,t.prev=n,s.next=n,n.prev=s,n}function O0(r,e,t,n){const i=new Zd(r,e,t);return n?(i.next=n.next,i.prev=n,n.next.prev=i,n.next=i):(i.prev=i,i.next=i),i}function Xa(r){r.next.prev=r.prev,r.prev.next=r.next,r.prevZ&&(r.prevZ.nextZ=r.nextZ),r.nextZ&&(r.nextZ.prevZ=r.prevZ)}function Zd(r,e,t){this.i=r,this.x=e,this.y=t,this.prev=null,this.next=null,this.z=0,this.prevZ=null,this.nextZ=null,this.steiner=!1}function UA(r,e,t,n){let i=0;for(let s=e,l=t-n;s<t;s+=n)i+=(r[l]-r[s])*(r[s+1]+r[l+1]),l=s;return i}class ji{static area(e){const t=e.length;let n=0;for(let i=t-1,s=0;s<t;i=s++)n+=e[i].x*e[s].y-e[s].x*e[i].y;return n*.5}static isClockWise(e){return ji.area(e)<0}static triangulateShape(e,t){const n=[],i=[],s=[];F0(e),B0(n,e);let l=e.length;t.forEach(F0);for(let u=0;u<t.length;u++)i.push(l),l+=t[u].length,B0(n,t[u]);const c=_A.triangulate(n,i);for(let u=0;u<c.length;u+=3)s.push(c.slice(u,u+3));return s}}function F0(r){const e=r.length;e>2&&r[e-1].equals(r[0])&&r.pop()}function B0(r,e){for(let t=0;t<e.length;t++)r.push(e[t].x),r.push(e[t].y)}class yh extends xt{constructor(e=new Rs([new ae(.5,.5),new ae(-.5,.5),new ae(-.5,-.5),new ae(.5,-.5)]),t={}){super(),this.type="ExtrudeGeometry",this.parameters={shapes:e,options:t},e=Array.isArray(e)?e:[e];const n=this,i=[],s=[];for(let c=0,u=e.length;c<u;c++){const h=e[c];l(h)}this.setAttribute("position",new Ye(i,3)),this.setAttribute("uv",new Ye(s,2)),this.computeVertexNormals();function l(c){const u=[],h=t.curveSegments!==void 0?t.curveSegments:12,f=t.steps!==void 0?t.steps:1,p=t.depth!==void 0?t.depth:1;let m=t.bevelEnabled!==void 0?t.bevelEnabled:!0,g=t.bevelThickness!==void 0?t.bevelThickness:.2,y=t.bevelSize!==void 0?t.bevelSize:g-.1,M=t.bevelOffset!==void 0?t.bevelOffset:0,x=t.bevelSegments!==void 0?t.bevelSegments:3;const _=t.extrudePath,w=t.UVGenerator!==void 0?t.UVGenerator:NA;let E,T=!1,U,P,D,F;_&&(E=_.getSpacedPoints(f),T=!0,m=!1,U=_.computeFrenetFrames(f,!1),P=new L,D=new L,F=new L),m||(x=0,g=0,y=0,M=0);const C=c.extractPoints(h);let b=C.shape;const N=C.holes;if(!ji.isClockWise(b)){b=b.reverse();for(let he=0,de=N.length;he<de;he++){const z=N[he];ji.isClockWise(z)&&(N[he]=z.reverse())}}const Y=ji.triangulateShape(b,N),K=b;for(let he=0,de=N.length;he<de;he++){const z=N[he];b=b.concat(z)}function le(he,de,z){return de||console.error("THREE.ExtrudeGeometry: vec does not exist"),he.clone().addScaledVector(de,z)}const $=b.length,pe=Y.length;function J(he,de,z){let je,ve,Oe;const Te=he.x-de.x,it=he.y-de.y,Pe=z.x-he.x,O=z.y-he.y,R=Te*Te+it*it,Z=Te*O-it*Pe;if(Math.abs(Z)>Number.EPSILON){const re=Math.sqrt(R),fe=Math.sqrt(Pe*Pe+O*O),ce=de.x-it/re,We=de.y+Te/re,Ae=z.x-O/fe,Fe=z.y+Pe/fe,St=((Ae-ce)*O-(Fe-We)*Pe)/(Te*O-it*Pe);je=ce+Te*St-he.x,ve=We+it*St-he.y;const _e=je*je+ve*ve;if(_e<=2)return new ae(je,ve);Oe=Math.sqrt(_e/2)}else{let re=!1;Te>Number.EPSILON?Pe>Number.EPSILON&&(re=!0):Te<-Number.EPSILON?Pe<-Number.EPSILON&&(re=!0):Math.sign(it)===Math.sign(O)&&(re=!0),re?(je=-it,ve=Te,Oe=Math.sqrt(R)):(je=Te,ve=it,Oe=Math.sqrt(R/2))}return new ae(je/Oe,ve/Oe)}const xe=[];for(let he=0,de=K.length,z=de-1,je=he+1;he<de;he++,z++,je++)z===de&&(z=0),je===de&&(je=0),xe[he]=J(K[he],K[z],K[je]);const me=[];let Se,Qe=xe.concat();for(let he=0,de=N.length;he<de;he++){const z=N[he];Se=[];for(let je=0,ve=z.length,Oe=ve-1,Te=je+1;je<ve;je++,Oe++,Te++)Oe===ve&&(Oe=0),Te===ve&&(Te=0),Se[je]=J(z[je],z[Oe],z[Te]);me.push(Se),Qe=Qe.concat(Se)}for(let he=0;he<x;he++){const de=he/x,z=g*Math.cos(de*Math.PI/2),je=y*Math.sin(de*Math.PI/2)+M;for(let ve=0,Oe=K.length;ve<Oe;ve++){const Te=le(K[ve],xe[ve],je);we(Te.x,Te.y,-z)}for(let ve=0,Oe=N.length;ve<Oe;ve++){const Te=N[ve];Se=me[ve];for(let it=0,Pe=Te.length;it<Pe;it++){const O=le(Te[it],Se[it],je);we(O.x,O.y,-z)}}}const Je=y+M;for(let he=0;he<$;he++){const de=m?le(b[he],Qe[he],Je):b[he];T?(D.copy(U.normals[0]).multiplyScalar(de.x),P.copy(U.binormals[0]).multiplyScalar(de.y),F.copy(E[0]).add(D).add(P),we(F.x,F.y,F.z)):we(de.x,de.y,0)}for(let he=1;he<=f;he++)for(let de=0;de<$;de++){const z=m?le(b[de],Qe[de],Je):b[de];T?(D.copy(U.normals[he]).multiplyScalar(z.x),P.copy(U.binormals[he]).multiplyScalar(z.y),F.copy(E[he]).add(D).add(P),we(F.x,F.y,F.z)):we(z.x,z.y,p/f*he)}for(let he=x-1;he>=0;he--){const de=he/x,z=g*Math.cos(de*Math.PI/2),je=y*Math.sin(de*Math.PI/2)+M;for(let ve=0,Oe=K.length;ve<Oe;ve++){const Te=le(K[ve],xe[ve],je);we(Te.x,Te.y,p+z)}for(let ve=0,Oe=N.length;ve<Oe;ve++){const Te=N[ve];Se=me[ve];for(let it=0,Pe=Te.length;it<Pe;it++){const O=le(Te[it],Se[it],je);T?we(O.x,O.y+E[f-1].y,E[f-1].x+z):we(O.x,O.y,p+z)}}}se(),ge();function se(){const he=i.length/3;if(m){let de=0,z=$*de;for(let je=0;je<pe;je++){const ve=Y[je];et(ve[2]+z,ve[1]+z,ve[0]+z)}de=f+x*2,z=$*de;for(let je=0;je<pe;je++){const ve=Y[je];et(ve[0]+z,ve[1]+z,ve[2]+z)}}else{for(let de=0;de<pe;de++){const z=Y[de];et(z[2],z[1],z[0])}for(let de=0;de<pe;de++){const z=Y[de];et(z[0]+$*f,z[1]+$*f,z[2]+$*f)}}n.addGroup(he,i.length/3-he,0)}function ge(){const he=i.length/3;let de=0;Ve(K,de),de+=K.length;for(let z=0,je=N.length;z<je;z++){const ve=N[z];Ve(ve,de),de+=ve.length}n.addGroup(he,i.length/3-he,1)}function Ve(he,de){let z=he.length;for(;--z>=0;){const je=z;let ve=z-1;ve<0&&(ve=he.length-1);for(let Oe=0,Te=f+x*2;Oe<Te;Oe++){const it=$*Oe,Pe=$*(Oe+1),O=de+je+it,R=de+ve+it,Z=de+ve+Pe,re=de+je+Pe;lt(O,R,Z,re)}}}function we(he,de,z){u.push(he),u.push(de),u.push(z)}function et(he,de,z){tt(he),tt(de),tt(z);const je=i.length/3,ve=w.generateTopUV(n,i,je-3,je-2,je-1);ft(ve[0]),ft(ve[1]),ft(ve[2])}function lt(he,de,z,je){tt(he),tt(de),tt(je),tt(de),tt(z),tt(je);const ve=i.length/3,Oe=w.generateSideWallUV(n,i,ve-6,ve-3,ve-2,ve-1);ft(Oe[0]),ft(Oe[1]),ft(Oe[3]),ft(Oe[1]),ft(Oe[2]),ft(Oe[3])}function tt(he){i.push(u[he*3+0]),i.push(u[he*3+1]),i.push(u[he*3+2])}function ft(he){s.push(he.x),s.push(he.y)}}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}toJSON(){const e=super.toJSON(),t=this.parameters.shapes,n=this.parameters.options;return OA(t,n,e)}static fromJSON(e,t){const n=[];for(let s=0,l=e.shapes.length;s<l;s++){const c=t[e.shapes[s]];n.push(c)}const i=e.options.extrudePath;return i!==void 0&&(e.options.extrudePath=new Zu[i.type]().fromJSON(i)),new yh(n,e.options)}}const NA={generateTopUV:function(r,e,t,n,i){const s=e[t*3],l=e[t*3+1],c=e[n*3],u=e[n*3+1],h=e[i*3],f=e[i*3+1];return[new ae(s,l),new ae(c,u),new ae(h,f)]},generateSideWallUV:function(r,e,t,n,i,s){const l=e[t*3],c=e[t*3+1],u=e[t*3+2],h=e[n*3],f=e[n*3+1],p=e[n*3+2],m=e[i*3],g=e[i*3+1],y=e[i*3+2],M=e[s*3],x=e[s*3+1],_=e[s*3+2];return Math.abs(c-f)<Math.abs(l-h)?[new ae(l,1-u),new ae(h,1-p),new ae(m,1-y),new ae(M,1-_)]:[new ae(c,1-u),new ae(f,1-p),new ae(g,1-y),new ae(x,1-_)]}};function OA(r,e,t){if(t.shapes=[],Array.isArray(r))for(let n=0,i=r.length;n<i;n++){const s=r[n];t.shapes.push(s.uuid)}else t.shapes.push(r.uuid);return t.options=Object.assign({},e),e.extrudePath!==void 0&&(t.options.extrudePath=e.extrudePath.toJSON()),t}class xh extends Xr{constructor(e=1,t=0){const n=(1+Math.sqrt(5))/2,i=[-1,n,0,1,n,0,-1,-n,0,1,-n,0,0,-1,n,0,1,n,0,-1,-n,0,1,-n,n,0,-1,n,0,1,-n,0,-1,-n,0,1],s=[0,11,5,0,5,1,0,1,7,0,7,10,0,10,11,1,5,9,5,11,4,11,10,2,10,7,6,7,1,8,3,9,4,3,4,2,3,2,6,3,6,8,3,8,9,4,9,5,2,4,11,6,2,10,8,6,7,9,8,1];super(i,s,e,t),this.type="IcosahedronGeometry",this.parameters={radius:e,detail:t}}static fromJSON(e){return new xh(e.radius,e.detail)}}class rl extends Xr{constructor(e=1,t=0){const n=[1,0,0,-1,0,0,0,1,0,0,-1,0,0,0,1,0,0,-1],i=[0,2,4,0,4,3,0,3,5,0,5,2,1,2,5,1,5,3,1,3,4,1,4,2];super(n,i,e,t),this.type="OctahedronGeometry",this.parameters={radius:e,detail:t}}static fromJSON(e){return new rl(e.radius,e.detail)}}class Sh extends xt{constructor(e=.5,t=1,n=32,i=1,s=0,l=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:n,phiSegments:i,thetaStart:s,thetaLength:l},n=Math.max(3,n),i=Math.max(1,i);const c=[],u=[],h=[],f=[];let p=e;const m=(t-e)/i,g=new L,y=new ae;for(let M=0;M<=i;M++){for(let x=0;x<=n;x++){const _=s+x/n*l;g.x=p*Math.cos(_),g.y=p*Math.sin(_),u.push(g.x,g.y,g.z),h.push(0,0,1),y.x=(g.x/t+1)/2,y.y=(g.y/t+1)/2,f.push(y.x,y.y)}p+=m}for(let M=0;M<i;M++){const x=M*(n+1);for(let _=0;_<n;_++){const w=_+x,E=w,T=w+n+1,U=w+n+2,P=w+1;c.push(E,T,P),c.push(T,U,P)}}this.setIndex(c),this.setAttribute("position",new Ye(u,3)),this.setAttribute("normal",new Ye(h,3)),this.setAttribute("uv",new Ye(f,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Sh(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class Mh extends xt{constructor(e=new Rs([new ae(0,.5),new ae(-.5,-.5),new ae(.5,-.5)]),t=12){super(),this.type="ShapeGeometry",this.parameters={shapes:e,curveSegments:t};const n=[],i=[],s=[],l=[];let c=0,u=0;if(Array.isArray(e)===!1)h(e);else for(let f=0;f<e.length;f++)h(e[f]),this.addGroup(c,u,f),c+=u,u=0;this.setIndex(n),this.setAttribute("position",new Ye(i,3)),this.setAttribute("normal",new Ye(s,3)),this.setAttribute("uv",new Ye(l,2));function h(f){const p=i.length/3,m=f.extractPoints(t);let g=m.shape;const y=m.holes;ji.isClockWise(g)===!1&&(g=g.reverse());for(let x=0,_=y.length;x<_;x++){const w=y[x];ji.isClockWise(w)===!0&&(y[x]=w.reverse())}const M=ji.triangulateShape(g,y);for(let x=0,_=y.length;x<_;x++){const w=y[x];g=g.concat(w)}for(let x=0,_=g.length;x<_;x++){const w=g[x];i.push(w.x,w.y,0),s.push(0,0,1),l.push(w.x,w.y)}for(let x=0,_=M.length;x<_;x++){const w=M[x],E=w[0]+p,T=w[1]+p,U=w[2]+p;n.push(E,T,U),u+=3}}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}toJSON(){const e=super.toJSON(),t=this.parameters.shapes;return FA(t,e)}static fromJSON(e,t){const n=[];for(let i=0,s=e.shapes.length;i<s;i++){const l=t[e.shapes[i]];n.push(l)}return new Mh(n,e.curveSegments)}}function FA(r,e){if(e.shapes=[],Array.isArray(r))for(let t=0,n=r.length;t<n;t++){const i=r[t];e.shapes.push(i.uuid)}else e.shapes.push(r.uuid);return e}class sl extends xt{constructor(e=1,t=32,n=16,i=0,s=Math.PI*2,l=0,c=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:n,phiStart:i,phiLength:s,thetaStart:l,thetaLength:c},t=Math.max(3,Math.floor(t)),n=Math.max(2,Math.floor(n));const u=Math.min(l+c,Math.PI);let h=0;const f=[],p=new L,m=new L,g=[],y=[],M=[],x=[];for(let _=0;_<=n;_++){const w=[],E=_/n;let T=0;_===0&&l===0?T=.5/t:_===n&&u===Math.PI&&(T=-.5/t);for(let U=0;U<=t;U++){const P=U/t;p.x=-e*Math.cos(i+P*s)*Math.sin(l+E*c),p.y=e*Math.cos(l+E*c),p.z=e*Math.sin(i+P*s)*Math.sin(l+E*c),y.push(p.x,p.y,p.z),m.copy(p).normalize(),M.push(m.x,m.y,m.z),x.push(P+T,1-E),w.push(h++)}f.push(w)}for(let _=0;_<n;_++)for(let w=0;w<t;w++){const E=f[_][w+1],T=f[_][w],U=f[_+1][w],P=f[_+1][w+1];(_!==0||l>0)&&g.push(E,T,P),(_!==n-1||u<Math.PI)&&g.push(T,U,P)}this.setIndex(g),this.setAttribute("position",new Ye(y,3)),this.setAttribute("normal",new Ye(M,3)),this.setAttribute("uv",new Ye(x,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new sl(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class Eh extends Xr{constructor(e=1,t=0){const n=[1,1,1,-1,-1,1,-1,1,-1,1,-1,-1],i=[2,1,0,0,3,2,1,3,0,2,3,1];super(n,i,e,t),this.type="TetrahedronGeometry",this.parameters={radius:e,detail:t}}static fromJSON(e){return new Eh(e.radius,e.detail)}}class wh extends xt{constructor(e=1,t=.4,n=12,i=48,s=Math.PI*2){super(),this.type="TorusGeometry",this.parameters={radius:e,tube:t,radialSegments:n,tubularSegments:i,arc:s},n=Math.floor(n),i=Math.floor(i);const l=[],c=[],u=[],h=[],f=new L,p=new L,m=new L;for(let g=0;g<=n;g++)for(let y=0;y<=i;y++){const M=y/i*s,x=g/n*Math.PI*2;p.x=(e+t*Math.cos(x))*Math.cos(M),p.y=(e+t*Math.cos(x))*Math.sin(M),p.z=t*Math.sin(x),c.push(p.x,p.y,p.z),f.x=e*Math.cos(M),f.y=e*Math.sin(M),m.subVectors(p,f).normalize(),u.push(m.x,m.y,m.z),h.push(y/i),h.push(g/n)}for(let g=1;g<=n;g++)for(let y=1;y<=i;y++){const M=(i+1)*g+y-1,x=(i+1)*(g-1)+y-1,_=(i+1)*(g-1)+y,w=(i+1)*g+y;l.push(M,x,w),l.push(x,_,w)}this.setIndex(l),this.setAttribute("position",new Ye(c,3)),this.setAttribute("normal",new Ye(u,3)),this.setAttribute("uv",new Ye(h,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new wh(e.radius,e.tube,e.radialSegments,e.tubularSegments,e.arc)}}class Th extends xt{constructor(e=1,t=.4,n=64,i=8,s=2,l=3){super(),this.type="TorusKnotGeometry",this.parameters={radius:e,tube:t,tubularSegments:n,radialSegments:i,p:s,q:l},n=Math.floor(n),i=Math.floor(i);const c=[],u=[],h=[],f=[],p=new L,m=new L,g=new L,y=new L,M=new L,x=new L,_=new L;for(let E=0;E<=n;++E){const T=E/n*s*Math.PI*2;w(T,s,l,e,g),w(T+.01,s,l,e,y),x.subVectors(y,g),_.addVectors(y,g),M.crossVectors(x,_),_.crossVectors(M,x),M.normalize(),_.normalize();for(let U=0;U<=i;++U){const P=U/i*Math.PI*2,D=-t*Math.cos(P),F=t*Math.sin(P);p.x=g.x+(D*_.x+F*M.x),p.y=g.y+(D*_.y+F*M.y),p.z=g.z+(D*_.z+F*M.z),u.push(p.x,p.y,p.z),m.subVectors(p,g).normalize(),h.push(m.x,m.y,m.z),f.push(E/n),f.push(U/i)}}for(let E=1;E<=n;E++)for(let T=1;T<=i;T++){const U=(i+1)*(E-1)+(T-1),P=(i+1)*E+(T-1),D=(i+1)*E+T,F=(i+1)*(E-1)+T;c.push(U,P,F),c.push(P,D,F)}this.setIndex(c),this.setAttribute("position",new Ye(u,3)),this.setAttribute("normal",new Ye(h,3)),this.setAttribute("uv",new Ye(f,2));function w(E,T,U,P,D){const F=Math.cos(E),C=Math.sin(E),b=U/T*E,N=Math.cos(b);D.x=P*(2+N)*.5*F,D.y=P*(2+N)*C*.5,D.z=P*Math.sin(b)*.5}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Th(e.radius,e.tube,e.tubularSegments,e.radialSegments,e.p,e.q)}}class Ah extends xt{constructor(e=new Pp(new L(-1,-1,0),new L(-1,1,0),new L(1,1,0)),t=64,n=1,i=8,s=!1){super(),this.type="TubeGeometry",this.parameters={path:e,tubularSegments:t,radius:n,radialSegments:i,closed:s};const l=e.computeFrenetFrames(t,s);this.tangents=l.tangents,this.normals=l.normals,this.binormals=l.binormals;const c=new L,u=new L,h=new ae;let f=new L;const p=[],m=[],g=[],y=[];M(),this.setIndex(y),this.setAttribute("position",new Ye(p,3)),this.setAttribute("normal",new Ye(m,3)),this.setAttribute("uv",new Ye(g,2));function M(){for(let E=0;E<t;E++)x(E);x(s===!1?t:0),w(),_()}function x(E){f=e.getPointAt(E/t,f);const T=l.normals[E],U=l.binormals[E];for(let P=0;P<=i;P++){const D=P/i*Math.PI*2,F=Math.sin(D),C=-Math.cos(D);u.x=C*T.x+F*U.x,u.y=C*T.y+F*U.y,u.z=C*T.z+F*U.z,u.normalize(),m.push(u.x,u.y,u.z),c.x=f.x+n*u.x,c.y=f.y+n*u.y,c.z=f.z+n*u.z,p.push(c.x,c.y,c.z)}}function _(){for(let E=1;E<=t;E++)for(let T=1;T<=i;T++){const U=(i+1)*(E-1)+(T-1),P=(i+1)*E+(T-1),D=(i+1)*E+T,F=(i+1)*(E-1)+T;y.push(U,P,F),y.push(P,D,F)}}function w(){for(let E=0;E<=t;E++)for(let T=0;T<=i;T++)h.x=E/t,h.y=T/i,g.push(h.x,h.y)}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}toJSON(){const e=super.toJSON();return e.path=this.parameters.path.toJSON(),e}static fromJSON(e){return new Ah(new Zu[e.path.type]().fromJSON(e.path),e.tubularSegments,e.radius,e.radialSegments,e.closed)}}class Lp extends xt{constructor(e=null){if(super(),this.type="WireframeGeometry",this.parameters={geometry:e},e!==null){const t=[],n=new Set,i=new L,s=new L;if(e.index!==null){const l=e.attributes.position,c=e.index;let u=e.groups;u.length===0&&(u=[{start:0,count:c.count,materialIndex:0}]);for(let h=0,f=u.length;h<f;++h){const p=u[h],m=p.start,g=p.count;for(let y=m,M=m+g;y<M;y+=3)for(let x=0;x<3;x++){const _=c.getX(y+x),w=c.getX(y+(x+1)%3);i.fromBufferAttribute(l,_),s.fromBufferAttribute(l,w),z0(i,s,n)===!0&&(t.push(i.x,i.y,i.z),t.push(s.x,s.y,s.z))}}}else{const l=e.attributes.position;for(let c=0,u=l.count/3;c<u;c++)for(let h=0;h<3;h++){const f=3*c+h,p=3*c+(h+1)%3;i.fromBufferAttribute(l,f),s.fromBufferAttribute(l,p),z0(i,s,n)===!0&&(t.push(i.x,i.y,i.z),t.push(s.x,s.y,s.z))}}this.setAttribute("position",new Ye(t,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}function z0(r,e,t){const n=`${r.x},${r.y},${r.z}-${e.x},${e.y},${e.z}`,i=`${e.x},${e.y},${e.z}-${r.x},${r.y},${r.z}`;return t.has(n)===!0||t.has(i)===!0?!1:(t.add(n),t.add(i),!0)}var k0=Object.freeze({__proto__:null,BoxGeometry:Fs,CapsuleGeometry:ph,CircleGeometry:mh,ConeGeometry:gh,CylinderGeometry:ko,DodecahedronGeometry:vh,EdgesGeometry:Z_,ExtrudeGeometry:yh,IcosahedronGeometry:xh,LatheGeometry:il,OctahedronGeometry:rl,PlaneGeometry:Bo,PolyhedronGeometry:Xr,RingGeometry:Sh,ShapeGeometry:Mh,SphereGeometry:sl,TetrahedronGeometry:Eh,TorusGeometry:wh,TorusKnotGeometry:Th,TubeGeometry:Ah,WireframeGeometry:Lp});class Q_ extends Nn{static get type(){return"ShadowMaterial"}constructor(e){super(),this.isShadowMaterial=!0,this.color=new Be(0),this.transparent=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.fog=e.fog,this}}class $_ extends _i{static get type(){return"RawShaderMaterial"}constructor(e){super(e),this.isRawShaderMaterial=!0}}class Dp extends Nn{static get type(){return"MeshStandardMaterial"}constructor(e){super(),this.isMeshStandardMaterial=!0,this.defines={STANDARD:""},this.color=new Be(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Be(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new ai,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class ey extends Dp{static get type(){return"MeshPhysicalMaterial"}constructor(e){super(),this.isMeshPhysicalMaterial=!0,this.defines={STANDARD:"",PHYSICAL:""},this.anisotropyRotation=0,this.anisotropyMap=null,this.clearcoatMap=null,this.clearcoatRoughness=0,this.clearcoatRoughnessMap=null,this.clearcoatNormalScale=new ae(1,1),this.clearcoatNormalMap=null,this.ior=1.5,Object.defineProperty(this,"reflectivity",{get:function(){return Jt(2.5*(this.ior-1)/(this.ior+1),0,1)},set:function(t){this.ior=(1+.4*t)/(1-.4*t)}}),this.iridescenceMap=null,this.iridescenceIOR=1.3,this.iridescenceThicknessRange=[100,400],this.iridescenceThicknessMap=null,this.sheenColor=new Be(0),this.sheenColorMap=null,this.sheenRoughness=1,this.sheenRoughnessMap=null,this.transmissionMap=null,this.thickness=0,this.thicknessMap=null,this.attenuationDistance=1/0,this.attenuationColor=new Be(1,1,1),this.specularIntensity=1,this.specularIntensityMap=null,this.specularColor=new Be(1,1,1),this.specularColorMap=null,this._anisotropy=0,this._clearcoat=0,this._dispersion=0,this._iridescence=0,this._sheen=0,this._transmission=0,this.setValues(e)}get anisotropy(){return this._anisotropy}set anisotropy(e){this._anisotropy>0!=e>0&&this.version++,this._anisotropy=e}get clearcoat(){return this._clearcoat}set clearcoat(e){this._clearcoat>0!=e>0&&this.version++,this._clearcoat=e}get iridescence(){return this._iridescence}set iridescence(e){this._iridescence>0!=e>0&&this.version++,this._iridescence=e}get dispersion(){return this._dispersion}set dispersion(e){this._dispersion>0!=e>0&&this.version++,this._dispersion=e}get sheen(){return this._sheen}set sheen(e){this._sheen>0!=e>0&&this.version++,this._sheen=e}get transmission(){return this._transmission}set transmission(e){this._transmission>0!=e>0&&this.version++,this._transmission=e}copy(e){return super.copy(e),this.defines={STANDARD:"",PHYSICAL:""},this.anisotropy=e.anisotropy,this.anisotropyRotation=e.anisotropyRotation,this.anisotropyMap=e.anisotropyMap,this.clearcoat=e.clearcoat,this.clearcoatMap=e.clearcoatMap,this.clearcoatRoughness=e.clearcoatRoughness,this.clearcoatRoughnessMap=e.clearcoatRoughnessMap,this.clearcoatNormalMap=e.clearcoatNormalMap,this.clearcoatNormalScale.copy(e.clearcoatNormalScale),this.dispersion=e.dispersion,this.ior=e.ior,this.iridescence=e.iridescence,this.iridescenceMap=e.iridescenceMap,this.iridescenceIOR=e.iridescenceIOR,this.iridescenceThicknessRange=[...e.iridescenceThicknessRange],this.iridescenceThicknessMap=e.iridescenceThicknessMap,this.sheen=e.sheen,this.sheenColor.copy(e.sheenColor),this.sheenColorMap=e.sheenColorMap,this.sheenRoughness=e.sheenRoughness,this.sheenRoughnessMap=e.sheenRoughnessMap,this.transmission=e.transmission,this.transmissionMap=e.transmissionMap,this.thickness=e.thickness,this.thicknessMap=e.thicknessMap,this.attenuationDistance=e.attenuationDistance,this.attenuationColor.copy(e.attenuationColor),this.specularIntensity=e.specularIntensity,this.specularIntensityMap=e.specularIntensityMap,this.specularColor.copy(e.specularColor),this.specularColorMap=e.specularColorMap,this}}class ty extends Nn{static get type(){return"MeshPhongMaterial"}constructor(e){super(),this.isMeshPhongMaterial=!0,this.color=new Be(16777215),this.specular=new Be(1118481),this.shininess=30,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Be(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new ai,this.combine=Ka,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.specular.copy(e.specular),this.shininess=e.shininess,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class ny extends Nn{static get type(){return"MeshToonMaterial"}constructor(e){super(),this.isMeshToonMaterial=!0,this.defines={TOON:""},this.color=new Be(16777215),this.map=null,this.gradientMap=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Be(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.alphaMap=null,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.gradientMap=e.gradientMap,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.alphaMap=e.alphaMap,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}class iy extends Nn{static get type(){return"MeshNormalMaterial"}constructor(e){super(),this.isMeshNormalMaterial=!0,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.flatShading=!1,this.setValues(e)}copy(e){return super.copy(e),this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.flatShading=e.flatShading,this}}class ry extends Nn{static get type(){return"MeshLambertMaterial"}constructor(e){super(),this.isMeshLambertMaterial=!0,this.color=new Be(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Be(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new ai,this.combine=Ka,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class sy extends Nn{static get type(){return"MeshMatcapMaterial"}constructor(e){super(),this.isMeshMatcapMaterial=!0,this.defines={MATCAP:""},this.color=new Be(16777215),this.matcap=null,this.map=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Gr,this.normalScale=new ae(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.alphaMap=null,this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={MATCAP:""},this.color.copy(e.color),this.matcap=e.matcap,this.map=e.map,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.alphaMap=e.alphaMap,this.flatShading=e.flatShading,this.fog=e.fog,this}}class oy extends Gn{static get type(){return"LineDashedMaterial"}constructor(e){super(),this.isLineDashedMaterial=!0,this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}function ws(r,e,t){return!r||!t&&r.constructor===e?r:typeof e.BYTES_PER_ELEMENT=="number"?new e(r):Array.prototype.slice.call(r)}function ay(r){return ArrayBuffer.isView(r)&&!(r instanceof DataView)}function ly(r){function e(i,s){return r[i]-r[s]}const t=r.length,n=new Array(t);for(let i=0;i!==t;++i)n[i]=i;return n.sort(e),n}function jd(r,e,t){const n=r.length,i=new r.constructor(n);for(let s=0,l=0;l!==n;++s){const c=t[s]*e;for(let u=0;u!==e;++u)i[l++]=r[c+u]}return i}function Up(r,e,t,n){let i=1,s=r[0];for(;s!==void 0&&s[n]===void 0;)s=r[i++];if(s===void 0)return;let l=s[n];if(l!==void 0)if(Array.isArray(l))do l=s[n],l!==void 0&&(e.push(s.time),t.push.apply(t,l)),s=r[i++];while(s!==void 0);else if(l.toArray!==void 0)do l=s[n],l!==void 0&&(e.push(s.time),l.toArray(t,t.length)),s=r[i++];while(s!==void 0);else do l=s[n],l!==void 0&&(e.push(s.time),t.push(l)),s=r[i++];while(s!==void 0)}function BA(r,e,t,n,i=30){const s=r.clone();s.name=e;const l=[];for(let u=0;u<s.tracks.length;++u){const h=s.tracks[u],f=h.getValueSize(),p=[],m=[];for(let g=0;g<h.times.length;++g){const y=h.times[g]*i;if(!(y<t||y>=n)){p.push(h.times[g]);for(let M=0;M<f;++M)m.push(h.values[g*f+M])}}p.length!==0&&(h.times=ws(p,h.times.constructor),h.values=ws(m,h.values.constructor),l.push(h))}s.tracks=l;let c=1/0;for(let u=0;u<s.tracks.length;++u)c>s.tracks[u].times[0]&&(c=s.tracks[u].times[0]);for(let u=0;u<s.tracks.length;++u)s.tracks[u].shift(-1*c);return s.resetDuration(),s}function zA(r,e=0,t=r,n=30){n<=0&&(n=30);const i=t.tracks.length,s=e/n;for(let l=0;l<i;++l){const c=t.tracks[l],u=c.ValueTypeName;if(u==="bool"||u==="string")continue;const h=r.tracks.find(function(_){return _.name===c.name&&_.ValueTypeName===u});if(h===void 0)continue;let f=0;const p=c.getValueSize();c.createInterpolant.isInterpolantFactoryMethodGLTFCubicSpline&&(f=p/3);let m=0;const g=h.getValueSize();h.createInterpolant.isInterpolantFactoryMethodGLTFCubicSpline&&(m=g/3);const y=c.times.length-1;let M;if(s<=c.times[0]){const _=f,w=p-f;M=c.values.slice(_,w)}else if(s>=c.times[y]){const _=y*p+f,w=_+p-f;M=c.values.slice(_,w)}else{const _=c.createInterpolant(),w=f,E=p-f;_.evaluate(s),M=_.resultBuffer.slice(w,E)}u==="quaternion"&&new Un().fromArray(M).normalize().conjugate().toArray(M);const x=h.times.length;for(let _=0;_<x;++_){const w=_*g+m;if(u==="quaternion")Un.multiplyQuaternionsFlat(h.values,w,M,0,h.values,w);else{const E=g-m*2;for(let T=0;T<E;++T)h.values[w+T]-=M[T]}}}return r.blendMode=fp,r}const kA={convertArray:ws,isTypedArray:ay,getKeyframeOrder:ly,sortedArray:jd,flattenJSON:Up,subclip:BA,makeClipAdditive:zA};class ol{constructor(e,t,n,i){this.parameterPositions=e,this._cachedIndex=0,this.resultBuffer=i!==void 0?i:new t.constructor(n),this.sampleValues=t,this.valueSize=n,this.settings=null,this.DefaultSettings_={}}evaluate(e){const t=this.parameterPositions;let n=this._cachedIndex,i=t[n],s=t[n-1];e:{t:{let l;n:{i:if(!(e<i)){for(let c=n+2;;){if(i===void 0){if(e<s)break i;return n=t.length,this._cachedIndex=n,this.copySampleValue_(n-1)}if(n===c)break;if(s=i,i=t[++n],e<i)break t}l=t.length;break n}if(!(e>=s)){const c=t[1];e<c&&(n=2,s=c);for(let u=n-2;;){if(s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(n===u)break;if(i=s,s=t[--n-1],e>=s)break t}l=n,n=0;break n}break e}for(;n<l;){const c=n+l>>>1;e<t[c]?l=c:n=c+1}if(i=t[n],s=t[n-1],s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(i===void 0)return n=t.length,this._cachedIndex=n,this.copySampleValue_(n-1)}this._cachedIndex=n,this.intervalChanged_(n,s,i)}return this.interpolate_(n,s,e,i)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(e){const t=this.resultBuffer,n=this.sampleValues,i=this.valueSize,s=e*i;for(let l=0;l!==i;++l)t[l]=n[s+l];return t}interpolate_(){throw new Error("call to abstract method")}intervalChanged_(){}}class cy extends ol{constructor(e,t,n,i){super(e,t,n,i),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:Ss,endingEnd:Ss}}intervalChanged_(e,t,n){const i=this.parameterPositions;let s=e-2,l=e+1,c=i[s],u=i[l];if(c===void 0)switch(this.getSettings_().endingStart){case Ms:s=e,c=2*t-n;break;case Ba:s=i.length-2,c=t+i[s]-i[s+1];break;default:s=e,c=n}if(u===void 0)switch(this.getSettings_().endingEnd){case Ms:l=e,u=2*n-t;break;case Ba:l=1,u=n+i[1]-i[0];break;default:l=e-1,u=t}const h=(n-t)*.5,f=this.valueSize;this._weightPrev=h/(t-c),this._weightNext=h/(u-n),this._offsetPrev=s*f,this._offsetNext=l*f}interpolate_(e,t,n,i){const s=this.resultBuffer,l=this.sampleValues,c=this.valueSize,u=e*c,h=u-c,f=this._offsetPrev,p=this._offsetNext,m=this._weightPrev,g=this._weightNext,y=(n-t)/(i-t),M=y*y,x=M*y,_=-m*x+2*m*M-m*y,w=(1+m)*x+(-1.5-2*m)*M+(-.5+m)*y+1,E=(-1-g)*x+(1.5+g)*M+.5*y,T=g*x-g*M;for(let U=0;U!==c;++U)s[U]=_*l[f+U]+w*l[h+U]+E*l[u+U]+T*l[p+U];return s}}class Np extends ol{constructor(e,t,n,i){super(e,t,n,i)}interpolate_(e,t,n,i){const s=this.resultBuffer,l=this.sampleValues,c=this.valueSize,u=e*c,h=u-c,f=(n-t)/(i-t),p=1-f;for(let m=0;m!==c;++m)s[m]=l[h+m]*p+l[u+m]*f;return s}}class uy extends ol{constructor(e,t,n,i){super(e,t,n,i)}interpolate_(e){return this.copySampleValue_(e-1)}}class Pi{constructor(e,t,n,i){if(e===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(t===void 0||t.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+e);this.name=e,this.times=ws(t,this.TimeBufferType),this.values=ws(n,this.ValueBufferType),this.setInterpolation(i||this.DefaultInterpolation)}static toJSON(e){const t=e.constructor;let n;if(t.toJSON!==this.toJSON)n=t.toJSON(e);else{n={name:e.name,times:ws(e.times,Array),values:ws(e.values,Array)};const i=e.getInterpolation();i!==e.DefaultInterpolation&&(n.interpolation=i)}return n.type=e.ValueTypeName,n}InterpolantFactoryMethodDiscrete(e){return new uy(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodLinear(e){return new Np(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodSmooth(e){return new cy(this.times,this.values,this.getValueSize(),e)}setInterpolation(e){let t;switch(e){case Fa:t=this.InterpolantFactoryMethodDiscrete;break;case Wu:t=this.InterpolantFactoryMethodLinear;break;case ou:t=this.InterpolantFactoryMethodSmooth;break}if(t===void 0){const n="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(e!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(n);return console.warn("THREE.KeyframeTrack:",n),this}return this.createInterpolant=t,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return Fa;case this.InterpolantFactoryMethodLinear:return Wu;case this.InterpolantFactoryMethodSmooth:return ou}}getValueSize(){return this.values.length/this.times.length}shift(e){if(e!==0){const t=this.times;for(let n=0,i=t.length;n!==i;++n)t[n]+=e}return this}scale(e){if(e!==1){const t=this.times;for(let n=0,i=t.length;n!==i;++n)t[n]*=e}return this}trim(e,t){const n=this.times,i=n.length;let s=0,l=i-1;for(;s!==i&&n[s]<e;)++s;for(;l!==-1&&n[l]>t;)--l;if(++l,s!==0||l!==i){s>=l&&(l=Math.max(l,1),s=l-1);const c=this.getValueSize();this.times=n.slice(s,l),this.values=this.values.slice(s*c,l*c)}return this}validate(){let e=!0;const t=this.getValueSize();t-Math.floor(t)!==0&&(console.error("THREE.KeyframeTrack: Invalid value size in track.",this),e=!1);const n=this.times,i=this.values,s=n.length;s===0&&(console.error("THREE.KeyframeTrack: Track is empty.",this),e=!1);let l=null;for(let c=0;c!==s;c++){const u=n[c];if(typeof u=="number"&&isNaN(u)){console.error("THREE.KeyframeTrack: Time is not a valid number.",this,c,u),e=!1;break}if(l!==null&&l>u){console.error("THREE.KeyframeTrack: Out of order keys.",this,c,u,l),e=!1;break}l=u}if(i!==void 0&&ay(i))for(let c=0,u=i.length;c!==u;++c){const h=i[c];if(isNaN(h)){console.error("THREE.KeyframeTrack: Value is not a valid number.",this,c,h),e=!1;break}}return e}optimize(){const e=this.times.slice(),t=this.values.slice(),n=this.getValueSize(),i=this.getInterpolation()===ou,s=e.length-1;let l=1;for(let c=1;c<s;++c){let u=!1;const h=e[c],f=e[c+1];if(h!==f&&(c!==1||h!==e[0]))if(i)u=!0;else{const p=c*n,m=p-n,g=p+n;for(let y=0;y!==n;++y){const M=t[p+y];if(M!==t[m+y]||M!==t[g+y]){u=!0;break}}}if(u){if(c!==l){e[l]=e[c];const p=c*n,m=l*n;for(let g=0;g!==n;++g)t[m+g]=t[p+g]}++l}}if(s>0){e[l]=e[s];for(let c=s*n,u=l*n,h=0;h!==n;++h)t[u+h]=t[c+h];++l}return l!==e.length?(this.times=e.slice(0,l),this.values=t.slice(0,l*n)):(this.times=e,this.values=t),this}clone(){const e=this.times.slice(),t=this.values.slice(),n=this.constructor,i=new n(this.name,e,t);return i.createInterpolant=this.createInterpolant,i}}Pi.prototype.TimeBufferType=Float32Array;Pi.prototype.ValueBufferType=Float32Array;Pi.prototype.DefaultInterpolation=Wu;class Bs extends Pi{constructor(e,t,n){super(e,t,n)}}Bs.prototype.ValueTypeName="bool";Bs.prototype.ValueBufferType=Array;Bs.prototype.DefaultInterpolation=Fa;Bs.prototype.InterpolantFactoryMethodLinear=void 0;Bs.prototype.InterpolantFactoryMethodSmooth=void 0;class Op extends Pi{}Op.prototype.ValueTypeName="color";class Ya extends Pi{}Ya.prototype.ValueTypeName="number";class hy extends ol{constructor(e,t,n,i){super(e,t,n,i)}interpolate_(e,t,n,i){const s=this.resultBuffer,l=this.sampleValues,c=this.valueSize,u=(n-t)/(i-t);let h=e*c;for(let f=h+c;h!==f;h+=4)Un.slerpFlat(s,0,l,h-c,l,h,u);return s}}class al extends Pi{InterpolantFactoryMethodLinear(e){return new hy(this.times,this.values,this.getValueSize(),e)}}al.prototype.ValueTypeName="quaternion";al.prototype.InterpolantFactoryMethodSmooth=void 0;class zs extends Pi{constructor(e,t,n){super(e,t,n)}}zs.prototype.ValueTypeName="string";zs.prototype.ValueBufferType=Array;zs.prototype.DefaultInterpolation=Fa;zs.prototype.InterpolantFactoryMethodLinear=void 0;zs.prototype.InterpolantFactoryMethodSmooth=void 0;class qa extends Pi{}qa.prototype.ValueTypeName="vector";class Za{constructor(e="",t=-1,n=[],i=sh){this.name=e,this.tracks=n,this.duration=t,this.blendMode=i,this.uuid=oi(),this.duration<0&&this.resetDuration()}static parse(e){const t=[],n=e.tracks,i=1/(e.fps||1);for(let l=0,c=n.length;l!==c;++l)t.push(VA(n[l]).scale(i));const s=new this(e.name,e.duration,t,e.blendMode);return s.uuid=e.uuid,s}static toJSON(e){const t=[],n=e.tracks,i={name:e.name,duration:e.duration,tracks:t,uuid:e.uuid,blendMode:e.blendMode};for(let s=0,l=n.length;s!==l;++s)t.push(Pi.toJSON(n[s]));return i}static CreateFromMorphTargetSequence(e,t,n,i){const s=t.length,l=[];for(let c=0;c<s;c++){let u=[],h=[];u.push((c+s-1)%s,c,(c+1)%s),h.push(0,1,0);const f=ly(u);u=jd(u,1,f),h=jd(h,1,f),!i&&u[0]===0&&(u.push(s),h.push(h[0])),l.push(new Ya(".morphTargetInfluences["+t[c].name+"]",u,h).scale(1/n))}return new this(e,-1,l)}static findByName(e,t){let n=e;if(!Array.isArray(e)){const i=e;n=i.geometry&&i.geometry.animations||i.animations}for(let i=0;i<n.length;i++)if(n[i].name===t)return n[i];return null}static CreateClipsFromMorphTargetSequences(e,t,n){const i={},s=/^([\w-]*?)([\d]+)$/;for(let c=0,u=e.length;c<u;c++){const h=e[c],f=h.name.match(s);if(f&&f.length>1){const p=f[1];let m=i[p];m||(i[p]=m=[]),m.push(h)}}const l=[];for(const c in i)l.push(this.CreateFromMorphTargetSequence(c,i[c],t,n));return l}static parseAnimation(e,t){if(!e)return console.error("THREE.AnimationClip: No animation in JSONLoader data."),null;const n=function(p,m,g,y,M){if(g.length!==0){const x=[],_=[];Up(g,x,_,y),x.length!==0&&M.push(new p(m,x,_))}},i=[],s=e.name||"default",l=e.fps||30,c=e.blendMode;let u=e.length||-1;const h=e.hierarchy||[];for(let p=0;p<h.length;p++){const m=h[p].keys;if(!(!m||m.length===0))if(m[0].morphTargets){const g={};let y;for(y=0;y<m.length;y++)if(m[y].morphTargets)for(let M=0;M<m[y].morphTargets.length;M++)g[m[y].morphTargets[M]]=-1;for(const M in g){const x=[],_=[];for(let w=0;w!==m[y].morphTargets.length;++w){const E=m[y];x.push(E.time),_.push(E.morphTarget===M?1:0)}i.push(new Ya(".morphTargetInfluence["+M+"]",x,_))}u=g.length*l}else{const g=".bones["+t[p].name+"]";n(qa,g+".position",m,"pos",i),n(al,g+".quaternion",m,"rot",i),n(qa,g+".scale",m,"scl",i)}}return i.length===0?null:new this(s,u,i,c)}resetDuration(){const e=this.tracks;let t=0;for(let n=0,i=e.length;n!==i;++n){const s=this.tracks[n];t=Math.max(t,s.times[s.times.length-1])}return this.duration=t,this}trim(){for(let e=0;e<this.tracks.length;e++)this.tracks[e].trim(0,this.duration);return this}validate(){let e=!0;for(let t=0;t<this.tracks.length;t++)e=e&&this.tracks[t].validate();return e}optimize(){for(let e=0;e<this.tracks.length;e++)this.tracks[e].optimize();return this}clone(){const e=[];for(let t=0;t<this.tracks.length;t++)e.push(this.tracks[t].clone());return new this.constructor(this.name,this.duration,e,this.blendMode)}toJSON(){return this.constructor.toJSON(this)}}function HA(r){switch(r.toLowerCase()){case"scalar":case"double":case"float":case"number":case"integer":return Ya;case"vector":case"vector2":case"vector3":case"vector4":return qa;case"color":return Op;case"quaternion":return al;case"bool":case"boolean":return Bs;case"string":return zs}throw new Error("THREE.KeyframeTrack: Unsupported typeName: "+r)}function VA(r){if(r.type===void 0)throw new Error("THREE.KeyframeTrack: track type undefined, can not parse");const e=HA(r.type);if(r.times===void 0){const t=[],n=[];Up(r.keys,t,n,"value"),r.times=t,r.values=n}return e.parse!==void 0?e.parse(r):new e(r.name,r.times,r.values,r.interpolation)}const pr={enabled:!1,files:{},add:function(r,e){this.enabled!==!1&&(this.files[r]=e)},get:function(r){if(this.enabled!==!1)return this.files[r]},remove:function(r){delete this.files[r]},clear:function(){this.files={}}};class Fp{constructor(e,t,n){const i=this;let s=!1,l=0,c=0,u;const h=[];this.onStart=void 0,this.onLoad=e,this.onProgress=t,this.onError=n,this.itemStart=function(f){c++,s===!1&&i.onStart!==void 0&&i.onStart(f,l,c),s=!0},this.itemEnd=function(f){l++,i.onProgress!==void 0&&i.onProgress(f,l,c),l===c&&(s=!1,i.onLoad!==void 0&&i.onLoad())},this.itemError=function(f){i.onError!==void 0&&i.onError(f)},this.resolveURL=function(f){return u?u(f):f},this.setURLModifier=function(f){return u=f,this},this.addHandler=function(f,p){return h.push(f,p),this},this.removeHandler=function(f){const p=h.indexOf(f);return p!==-1&&h.splice(p,2),this},this.getHandler=function(f){for(let p=0,m=h.length;p<m;p+=2){const g=h[p],y=h[p+1];if(g.global&&(g.lastIndex=0),g.test(f))return y}return null}}}const fy=new Fp;class Qn{constructor(e){this.manager=e!==void 0?e:fy,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={}}load(){}loadAsync(e,t){const n=this;return new Promise(function(i,s){n.load(e,i,t,s)})}parse(){}setCrossOrigin(e){return this.crossOrigin=e,this}setWithCredentials(e){return this.withCredentials=e,this}setPath(e){return this.path=e,this}setResourcePath(e){return this.resourcePath=e,this}setRequestHeader(e){return this.requestHeader=e,this}}Qn.DEFAULT_MATERIAL_NAME="__DEFAULT";const cr={};class GA extends Error{constructor(e,t){super(e),this.response=t}}class xr extends Qn{constructor(e){super(e)}load(e,t,n,i){e===void 0&&(e=""),this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);const s=pr.get(e);if(s!==void 0)return this.manager.itemStart(e),setTimeout(()=>{t&&t(s),this.manager.itemEnd(e)},0),s;if(cr[e]!==void 0){cr[e].push({onLoad:t,onProgress:n,onError:i});return}cr[e]=[],cr[e].push({onLoad:t,onProgress:n,onError:i});const l=new Request(e,{headers:new Headers(this.requestHeader),credentials:this.withCredentials?"include":"same-origin"}),c=this.mimeType,u=this.responseType;fetch(l).then(h=>{if(h.status===200||h.status===0){if(h.status===0&&console.warn("THREE.FileLoader: HTTP Status 0 received."),typeof ReadableStream>"u"||h.body===void 0||h.body.getReader===void 0)return h;const f=cr[e],p=h.body.getReader(),m=h.headers.get("X-File-Size")||h.headers.get("Content-Length"),g=m?parseInt(m):0,y=g!==0;let M=0;const x=new ReadableStream({start(_){w();function w(){p.read().then(({done:E,value:T})=>{if(E)_.close();else{M+=T.byteLength;const U=new ProgressEvent("progress",{lengthComputable:y,loaded:M,total:g});for(let P=0,D=f.length;P<D;P++){const F=f[P];F.onProgress&&F.onProgress(U)}_.enqueue(T),w()}},E=>{_.error(E)})}}});return new Response(x)}else throw new GA(`fetch for "${h.url}" responded with ${h.status}: ${h.statusText}`,h)}).then(h=>{switch(u){case"arraybuffer":return h.arrayBuffer();case"blob":return h.blob();case"document":return h.text().then(f=>new DOMParser().parseFromString(f,c));case"json":return h.json();default:if(c===void 0)return h.text();{const p=/charset="?([^;"\s]*)"?/i.exec(c),m=p&&p[1]?p[1].toLowerCase():void 0,g=new TextDecoder(m);return h.arrayBuffer().then(y=>g.decode(y))}}}).then(h=>{pr.add(e,h);const f=cr[e];delete cr[e];for(let p=0,m=f.length;p<m;p++){const g=f[p];g.onLoad&&g.onLoad(h)}}).catch(h=>{const f=cr[e];if(f===void 0)throw this.manager.itemError(e),h;delete cr[e];for(let p=0,m=f.length;p<m;p++){const g=f[p];g.onError&&g.onError(h)}this.manager.itemError(e)}).finally(()=>{this.manager.itemEnd(e)}),this.manager.itemStart(e)}setResponseType(e){return this.responseType=e,this}setMimeType(e){return this.mimeType=e,this}}class WA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=new xr(this.manager);l.setPath(this.path),l.setRequestHeader(this.requestHeader),l.setWithCredentials(this.withCredentials),l.load(e,function(c){try{t(s.parse(JSON.parse(c)))}catch(u){i?i(u):console.error(u),s.manager.itemError(e)}},n,i)}parse(e){const t=[];for(let n=0;n<e.length;n++){const i=Za.parse(e[n]);t.push(i)}return t}}class XA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=[],c=new fh,u=new xr(this.manager);u.setPath(this.path),u.setResponseType("arraybuffer"),u.setRequestHeader(this.requestHeader),u.setWithCredentials(s.withCredentials);let h=0;function f(p){u.load(e[p],function(m){const g=s.parse(m,!0);l[p]={width:g.width,height:g.height,format:g.format,mipmaps:g.mipmaps},h+=1,h===6&&(g.mipmapCount===1&&(c.minFilter=cn),c.image=l,c.format=g.format,c.needsUpdate=!0,t&&t(c))},n,i)}if(Array.isArray(e))for(let p=0,m=e.length;p<m;++p)f(p);else u.load(e,function(p){const m=s.parse(p,!0);if(m.isCubemap){const g=m.mipmaps.length/m.mipmapCount;for(let y=0;y<g;y++){l[y]={mipmaps:[]};for(let M=0;M<m.mipmapCount;M++)l[y].mipmaps.push(m.mipmaps[y*m.mipmapCount+M]),l[y].format=m.format,l[y].width=m.width,l[y].height=m.height}c.image=l}else c.image.width=m.width,c.image.height=m.height,c.mipmaps=m.mipmaps;m.mipmapCount===1&&(c.minFilter=cn),c.format=m.format,c.needsUpdate=!0,t&&t(c)},n,i);return c}}class ja extends Qn{constructor(e){super(e)}load(e,t,n,i){this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);const s=this,l=pr.get(e);if(l!==void 0)return s.manager.itemStart(e),setTimeout(function(){t&&t(l),s.manager.itemEnd(e)},0),l;const c=Ha("img");function u(){f(),pr.add(e,this),t&&t(this),s.manager.itemEnd(e)}function h(p){f(),i&&i(p),s.manager.itemError(e),s.manager.itemEnd(e)}function f(){c.removeEventListener("load",u,!1),c.removeEventListener("error",h,!1)}return c.addEventListener("load",u,!1),c.addEventListener("error",h,!1),e.slice(0,5)!=="data:"&&this.crossOrigin!==void 0&&(c.crossOrigin=this.crossOrigin),s.manager.itemStart(e),c.src=e,c}}class YA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=new tl;s.colorSpace=jn;const l=new ja(this.manager);l.setCrossOrigin(this.crossOrigin),l.setPath(this.path);let c=0;function u(h){l.load(e[h],function(f){s.images[h]=f,c++,c===6&&(s.needsUpdate=!0,t&&t(s))},void 0,i)}for(let h=0;h<e.length;++h)u(h);return s}}class qA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=new Zi,c=new xr(this.manager);return c.setResponseType("arraybuffer"),c.setRequestHeader(this.requestHeader),c.setPath(this.path),c.setWithCredentials(s.withCredentials),c.load(e,function(u){let h;try{h=s.parse(u)}catch(f){if(i!==void 0)i(f);else{console.error(f);return}}h.image!==void 0?l.image=h.image:h.data!==void 0&&(l.image.width=h.width,l.image.height=h.height,l.image.data=h.data),l.wrapS=h.wrapS!==void 0?h.wrapS:vi,l.wrapT=h.wrapT!==void 0?h.wrapT:vi,l.magFilter=h.magFilter!==void 0?h.magFilter:cn,l.minFilter=h.minFilter!==void 0?h.minFilter:cn,l.anisotropy=h.anisotropy!==void 0?h.anisotropy:1,h.colorSpace!==void 0&&(l.colorSpace=h.colorSpace),h.flipY!==void 0&&(l.flipY=h.flipY),h.format!==void 0&&(l.format=h.format),h.type!==void 0&&(l.type=h.type),h.mipmaps!==void 0&&(l.mipmaps=h.mipmaps,l.minFilter=Xi),h.mipmapCount===1&&(l.minFilter=cn),h.generateMipmaps!==void 0&&(l.generateMipmaps=h.generateMipmaps),l.needsUpdate=!0,t&&t(l,h)},n,i),l}}class ZA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=new Kt,l=new ja(this.manager);return l.setCrossOrigin(this.crossOrigin),l.setPath(this.path),l.load(e,function(c){s.image=c,s.needsUpdate=!0,t!==void 0&&t(s)},n,i),s}}class Yr extends Dt{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new Be(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}class dy extends Yr{constructor(e,t,n){super(e,n),this.isHemisphereLight=!0,this.type="HemisphereLight",this.position.copy(Dt.DEFAULT_UP),this.updateMatrix(),this.groundColor=new Be(t)}copy(e,t){return super.copy(e,t),this.groundColor.copy(e.groundColor),this}}const yd=new ut,H0=new L,V0=new L;class Bp{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new ae(512,512),this.map=null,this.mapPass=null,this.matrix=new ut,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new nl,this._frameExtents=new ae(1,1),this._viewportCount=1,this._viewports=[new At(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,n=this.matrix;H0.setFromMatrixPosition(e.matrixWorld),t.position.copy(H0),V0.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(V0),t.updateMatrixWorld(),yd.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(yd),n.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),n.multiply(yd)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class jA extends Bp{constructor(){super(new tn(50,1,.5,500)),this.isSpotLightShadow=!0,this.focus=1}updateMatrices(e){const t=this.camera,n=Lo*2*e.angle*this.focus,i=this.mapSize.width/this.mapSize.height,s=e.distance||t.far;(n!==t.fov||i!==t.aspect||s!==t.far)&&(t.fov=n,t.aspect=i,t.far=s,t.updateProjectionMatrix()),super.updateMatrices(e)}copy(e){return super.copy(e),this.focus=e.focus,this}}class py extends Yr{constructor(e,t,n=0,i=Math.PI/3,s=0,l=2){super(e,t),this.isSpotLight=!0,this.type="SpotLight",this.position.copy(Dt.DEFAULT_UP),this.updateMatrix(),this.target=new Dt,this.distance=n,this.angle=i,this.penumbra=s,this.decay=l,this.map=null,this.shadow=new jA}get power(){return this.intensity*Math.PI}set power(e){this.intensity=e/Math.PI}dispose(){this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.angle=e.angle,this.penumbra=e.penumbra,this.decay=e.decay,this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}const G0=new ut,va=new L,xd=new L;class JA extends Bp{constructor(){super(new tn(90,1,.5,500)),this.isPointLightShadow=!0,this._frameExtents=new ae(4,2),this._viewportCount=6,this._viewports=[new At(2,1,1,1),new At(0,1,1,1),new At(3,1,1,1),new At(1,1,1,1),new At(3,0,1,1),new At(1,0,1,1)],this._cubeDirections=[new L(1,0,0),new L(-1,0,0),new L(0,0,1),new L(0,0,-1),new L(0,1,0),new L(0,-1,0)],this._cubeUps=[new L(0,1,0),new L(0,1,0),new L(0,1,0),new L(0,1,0),new L(0,0,1),new L(0,0,-1)]}updateMatrices(e,t=0){const n=this.camera,i=this.matrix,s=e.distance||n.far;s!==n.far&&(n.far=s,n.updateProjectionMatrix()),va.setFromMatrixPosition(e.matrixWorld),n.position.copy(va),xd.copy(n.position),xd.add(this._cubeDirections[t]),n.up.copy(this._cubeUps[t]),n.lookAt(xd),n.updateMatrixWorld(),i.makeTranslation(-va.x,-va.y,-va.z),G0.multiplyMatrices(n.projectionMatrix,n.matrixWorldInverse),this._frustum.setFromProjectionMatrix(G0)}}class my extends Yr{constructor(e,t,n=0,i=2){super(e,t),this.isPointLight=!0,this.type="PointLight",this.distance=n,this.decay=i,this.shadow=new JA}get power(){return this.intensity*4*Math.PI}set power(e){this.intensity=e/(4*Math.PI)}dispose(){this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.decay=e.decay,this.shadow=e.shadow.clone(),this}}class KA extends Bp{constructor(){super(new kr(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class gy extends Yr{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Dt.DEFAULT_UP),this.updateMatrix(),this.target=new Dt,this.shadow=new KA}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class vy extends Yr{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class _y extends Yr{constructor(e,t,n=10,i=10){super(e,t),this.isRectAreaLight=!0,this.type="RectAreaLight",this.width=n,this.height=i}get power(){return this.intensity*this.width*this.height*Math.PI}set power(e){this.intensity=e/(this.width*this.height*Math.PI)}copy(e){return super.copy(e),this.width=e.width,this.height=e.height,this}toJSON(e){const t=super.toJSON(e);return t.object.width=this.width,t.object.height=this.height,t}}class yy{constructor(){this.isSphericalHarmonics3=!0,this.coefficients=[];for(let e=0;e<9;e++)this.coefficients.push(new L)}set(e){for(let t=0;t<9;t++)this.coefficients[t].copy(e[t]);return this}zero(){for(let e=0;e<9;e++)this.coefficients[e].set(0,0,0);return this}getAt(e,t){const n=e.x,i=e.y,s=e.z,l=this.coefficients;return t.copy(l[0]).multiplyScalar(.282095),t.addScaledVector(l[1],.488603*i),t.addScaledVector(l[2],.488603*s),t.addScaledVector(l[3],.488603*n),t.addScaledVector(l[4],1.092548*(n*i)),t.addScaledVector(l[5],1.092548*(i*s)),t.addScaledVector(l[6],.315392*(3*s*s-1)),t.addScaledVector(l[7],1.092548*(n*s)),t.addScaledVector(l[8],.546274*(n*n-i*i)),t}getIrradianceAt(e,t){const n=e.x,i=e.y,s=e.z,l=this.coefficients;return t.copy(l[0]).multiplyScalar(.886227),t.addScaledVector(l[1],2*.511664*i),t.addScaledVector(l[2],2*.511664*s),t.addScaledVector(l[3],2*.511664*n),t.addScaledVector(l[4],2*.429043*n*i),t.addScaledVector(l[5],2*.429043*i*s),t.addScaledVector(l[6],.743125*s*s-.247708),t.addScaledVector(l[7],2*.429043*n*s),t.addScaledVector(l[8],.429043*(n*n-i*i)),t}add(e){for(let t=0;t<9;t++)this.coefficients[t].add(e.coefficients[t]);return this}addScaledSH(e,t){for(let n=0;n<9;n++)this.coefficients[n].addScaledVector(e.coefficients[n],t);return this}scale(e){for(let t=0;t<9;t++)this.coefficients[t].multiplyScalar(e);return this}lerp(e,t){for(let n=0;n<9;n++)this.coefficients[n].lerp(e.coefficients[n],t);return this}equals(e){for(let t=0;t<9;t++)if(!this.coefficients[t].equals(e.coefficients[t]))return!1;return!0}copy(e){return this.set(e.coefficients)}clone(){return new this.constructor().copy(this)}fromArray(e,t=0){const n=this.coefficients;for(let i=0;i<9;i++)n[i].fromArray(e,t+i*3);return this}toArray(e=[],t=0){const n=this.coefficients;for(let i=0;i<9;i++)n[i].toArray(e,t+i*3);return e}static getBasisAt(e,t){const n=e.x,i=e.y,s=e.z;t[0]=.282095,t[1]=.488603*i,t[2]=.488603*s,t[3]=.488603*n,t[4]=1.092548*n*i,t[5]=1.092548*i*s,t[6]=.315392*(3*s*s-1),t[7]=1.092548*n*s,t[8]=.546274*(n*n-i*i)}}class xy extends Yr{constructor(e=new yy,t=1){super(void 0,t),this.isLightProbe=!0,this.sh=e}copy(e){return super.copy(e),this.sh.copy(e.sh),this}fromJSON(e){return this.intensity=e.intensity,this.sh.fromArray(e.sh),this}toJSON(e){const t=super.toJSON(e);return t.object.sh=this.sh.toArray(),t}}class bh extends Qn{constructor(e){super(e),this.textures={}}load(e,t,n,i){const s=this,l=new xr(s.manager);l.setPath(s.path),l.setRequestHeader(s.requestHeader),l.setWithCredentials(s.withCredentials),l.load(e,function(c){try{t(s.parse(JSON.parse(c)))}catch(u){i?i(u):console.error(u),s.manager.itemError(e)}},n,i)}parse(e){const t=this.textures;function n(s){return t[s]===void 0&&console.warn("THREE.MaterialLoader: Undefined texture",s),t[s]}const i=this.createMaterialFromType(e.type);if(e.uuid!==void 0&&(i.uuid=e.uuid),e.name!==void 0&&(i.name=e.name),e.color!==void 0&&i.color!==void 0&&i.color.setHex(e.color),e.roughness!==void 0&&(i.roughness=e.roughness),e.metalness!==void 0&&(i.metalness=e.metalness),e.sheen!==void 0&&(i.sheen=e.sheen),e.sheenColor!==void 0&&(i.sheenColor=new Be().setHex(e.sheenColor)),e.sheenRoughness!==void 0&&(i.sheenRoughness=e.sheenRoughness),e.emissive!==void 0&&i.emissive!==void 0&&i.emissive.setHex(e.emissive),e.specular!==void 0&&i.specular!==void 0&&i.specular.setHex(e.specular),e.specularIntensity!==void 0&&(i.specularIntensity=e.specularIntensity),e.specularColor!==void 0&&i.specularColor!==void 0&&i.specularColor.setHex(e.specularColor),e.shininess!==void 0&&(i.shininess=e.shininess),e.clearcoat!==void 0&&(i.clearcoat=e.clearcoat),e.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=e.clearcoatRoughness),e.dispersion!==void 0&&(i.dispersion=e.dispersion),e.iridescence!==void 0&&(i.iridescence=e.iridescence),e.iridescenceIOR!==void 0&&(i.iridescenceIOR=e.iridescenceIOR),e.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=e.iridescenceThicknessRange),e.transmission!==void 0&&(i.transmission=e.transmission),e.thickness!==void 0&&(i.thickness=e.thickness),e.attenuationDistance!==void 0&&(i.attenuationDistance=e.attenuationDistance),e.attenuationColor!==void 0&&i.attenuationColor!==void 0&&i.attenuationColor.setHex(e.attenuationColor),e.anisotropy!==void 0&&(i.anisotropy=e.anisotropy),e.anisotropyRotation!==void 0&&(i.anisotropyRotation=e.anisotropyRotation),e.fog!==void 0&&(i.fog=e.fog),e.flatShading!==void 0&&(i.flatShading=e.flatShading),e.blending!==void 0&&(i.blending=e.blending),e.combine!==void 0&&(i.combine=e.combine),e.side!==void 0&&(i.side=e.side),e.shadowSide!==void 0&&(i.shadowSide=e.shadowSide),e.opacity!==void 0&&(i.opacity=e.opacity),e.transparent!==void 0&&(i.transparent=e.transparent),e.alphaTest!==void 0&&(i.alphaTest=e.alphaTest),e.alphaHash!==void 0&&(i.alphaHash=e.alphaHash),e.depthFunc!==void 0&&(i.depthFunc=e.depthFunc),e.depthTest!==void 0&&(i.depthTest=e.depthTest),e.depthWrite!==void 0&&(i.depthWrite=e.depthWrite),e.colorWrite!==void 0&&(i.colorWrite=e.colorWrite),e.blendSrc!==void 0&&(i.blendSrc=e.blendSrc),e.blendDst!==void 0&&(i.blendDst=e.blendDst),e.blendEquation!==void 0&&(i.blendEquation=e.blendEquation),e.blendSrcAlpha!==void 0&&(i.blendSrcAlpha=e.blendSrcAlpha),e.blendDstAlpha!==void 0&&(i.blendDstAlpha=e.blendDstAlpha),e.blendEquationAlpha!==void 0&&(i.blendEquationAlpha=e.blendEquationAlpha),e.blendColor!==void 0&&i.blendColor!==void 0&&i.blendColor.setHex(e.blendColor),e.blendAlpha!==void 0&&(i.blendAlpha=e.blendAlpha),e.stencilWriteMask!==void 0&&(i.stencilWriteMask=e.stencilWriteMask),e.stencilFunc!==void 0&&(i.stencilFunc=e.stencilFunc),e.stencilRef!==void 0&&(i.stencilRef=e.stencilRef),e.stencilFuncMask!==void 0&&(i.stencilFuncMask=e.stencilFuncMask),e.stencilFail!==void 0&&(i.stencilFail=e.stencilFail),e.stencilZFail!==void 0&&(i.stencilZFail=e.stencilZFail),e.stencilZPass!==void 0&&(i.stencilZPass=e.stencilZPass),e.stencilWrite!==void 0&&(i.stencilWrite=e.stencilWrite),e.wireframe!==void 0&&(i.wireframe=e.wireframe),e.wireframeLinewidth!==void 0&&(i.wireframeLinewidth=e.wireframeLinewidth),e.wireframeLinecap!==void 0&&(i.wireframeLinecap=e.wireframeLinecap),e.wireframeLinejoin!==void 0&&(i.wireframeLinejoin=e.wireframeLinejoin),e.rotation!==void 0&&(i.rotation=e.rotation),e.linewidth!==void 0&&(i.linewidth=e.linewidth),e.dashSize!==void 0&&(i.dashSize=e.dashSize),e.gapSize!==void 0&&(i.gapSize=e.gapSize),e.scale!==void 0&&(i.scale=e.scale),e.polygonOffset!==void 0&&(i.polygonOffset=e.polygonOffset),e.polygonOffsetFactor!==void 0&&(i.polygonOffsetFactor=e.polygonOffsetFactor),e.polygonOffsetUnits!==void 0&&(i.polygonOffsetUnits=e.polygonOffsetUnits),e.dithering!==void 0&&(i.dithering=e.dithering),e.alphaToCoverage!==void 0&&(i.alphaToCoverage=e.alphaToCoverage),e.premultipliedAlpha!==void 0&&(i.premultipliedAlpha=e.premultipliedAlpha),e.forceSinglePass!==void 0&&(i.forceSinglePass=e.forceSinglePass),e.visible!==void 0&&(i.visible=e.visible),e.toneMapped!==void 0&&(i.toneMapped=e.toneMapped),e.userData!==void 0&&(i.userData=e.userData),e.vertexColors!==void 0&&(typeof e.vertexColors=="number"?i.vertexColors=e.vertexColors>0:i.vertexColors=e.vertexColors),e.uniforms!==void 0)for(const s in e.uniforms){const l=e.uniforms[s];switch(i.uniforms[s]={},l.type){case"t":i.uniforms[s].value=n(l.value);break;case"c":i.uniforms[s].value=new Be().setHex(l.value);break;case"v2":i.uniforms[s].value=new ae().fromArray(l.value);break;case"v3":i.uniforms[s].value=new L().fromArray(l.value);break;case"v4":i.uniforms[s].value=new At().fromArray(l.value);break;case"m3":i.uniforms[s].value=new gt().fromArray(l.value);break;case"m4":i.uniforms[s].value=new ut().fromArray(l.value);break;default:i.uniforms[s].value=l.value}}if(e.defines!==void 0&&(i.defines=e.defines),e.vertexShader!==void 0&&(i.vertexShader=e.vertexShader),e.fragmentShader!==void 0&&(i.fragmentShader=e.fragmentShader),e.glslVersion!==void 0&&(i.glslVersion=e.glslVersion),e.extensions!==void 0)for(const s in e.extensions)i.extensions[s]=e.extensions[s];if(e.lights!==void 0&&(i.lights=e.lights),e.clipping!==void 0&&(i.clipping=e.clipping),e.size!==void 0&&(i.size=e.size),e.sizeAttenuation!==void 0&&(i.sizeAttenuation=e.sizeAttenuation),e.map!==void 0&&(i.map=n(e.map)),e.matcap!==void 0&&(i.matcap=n(e.matcap)),e.alphaMap!==void 0&&(i.alphaMap=n(e.alphaMap)),e.bumpMap!==void 0&&(i.bumpMap=n(e.bumpMap)),e.bumpScale!==void 0&&(i.bumpScale=e.bumpScale),e.normalMap!==void 0&&(i.normalMap=n(e.normalMap)),e.normalMapType!==void 0&&(i.normalMapType=e.normalMapType),e.normalScale!==void 0){let s=e.normalScale;Array.isArray(s)===!1&&(s=[s,s]),i.normalScale=new ae().fromArray(s)}return e.displacementMap!==void 0&&(i.displacementMap=n(e.displacementMap)),e.displacementScale!==void 0&&(i.displacementScale=e.displacementScale),e.displacementBias!==void 0&&(i.displacementBias=e.displacementBias),e.roughnessMap!==void 0&&(i.roughnessMap=n(e.roughnessMap)),e.metalnessMap!==void 0&&(i.metalnessMap=n(e.metalnessMap)),e.emissiveMap!==void 0&&(i.emissiveMap=n(e.emissiveMap)),e.emissiveIntensity!==void 0&&(i.emissiveIntensity=e.emissiveIntensity),e.specularMap!==void 0&&(i.specularMap=n(e.specularMap)),e.specularIntensityMap!==void 0&&(i.specularIntensityMap=n(e.specularIntensityMap)),e.specularColorMap!==void 0&&(i.specularColorMap=n(e.specularColorMap)),e.envMap!==void 0&&(i.envMap=n(e.envMap)),e.envMapRotation!==void 0&&i.envMapRotation.fromArray(e.envMapRotation),e.envMapIntensity!==void 0&&(i.envMapIntensity=e.envMapIntensity),e.reflectivity!==void 0&&(i.reflectivity=e.reflectivity),e.refractionRatio!==void 0&&(i.refractionRatio=e.refractionRatio),e.lightMap!==void 0&&(i.lightMap=n(e.lightMap)),e.lightMapIntensity!==void 0&&(i.lightMapIntensity=e.lightMapIntensity),e.aoMap!==void 0&&(i.aoMap=n(e.aoMap)),e.aoMapIntensity!==void 0&&(i.aoMapIntensity=e.aoMapIntensity),e.gradientMap!==void 0&&(i.gradientMap=n(e.gradientMap)),e.clearcoatMap!==void 0&&(i.clearcoatMap=n(e.clearcoatMap)),e.clearcoatRoughnessMap!==void 0&&(i.clearcoatRoughnessMap=n(e.clearcoatRoughnessMap)),e.clearcoatNormalMap!==void 0&&(i.clearcoatNormalMap=n(e.clearcoatNormalMap)),e.clearcoatNormalScale!==void 0&&(i.clearcoatNormalScale=new ae().fromArray(e.clearcoatNormalScale)),e.iridescenceMap!==void 0&&(i.iridescenceMap=n(e.iridescenceMap)),e.iridescenceThicknessMap!==void 0&&(i.iridescenceThicknessMap=n(e.iridescenceThicknessMap)),e.transmissionMap!==void 0&&(i.transmissionMap=n(e.transmissionMap)),e.thicknessMap!==void 0&&(i.thicknessMap=n(e.thicknessMap)),e.anisotropyMap!==void 0&&(i.anisotropyMap=n(e.anisotropyMap)),e.sheenColorMap!==void 0&&(i.sheenColorMap=n(e.sheenColorMap)),e.sheenRoughnessMap!==void 0&&(i.sheenRoughnessMap=n(e.sheenRoughnessMap)),i}setTextures(e){return this.textures=e,this}createMaterialFromType(e){return bh.createMaterialFromType(e)}static createMaterialFromType(e){const t={ShadowMaterial:Q_,SpriteMaterial:Ep,RawShaderMaterial:$_,ShaderMaterial:_i,PointsMaterial:Tp,MeshPhysicalMaterial:ey,MeshStandardMaterial:Dp,MeshPhongMaterial:ty,MeshToonMaterial:ny,MeshNormalMaterial:iy,MeshLambertMaterial:ry,MeshDepthMaterial:xp,MeshDistanceMaterial:Sp,MeshBasicMaterial:Wr,MeshMatcapMaterial:sy,LineDashedMaterial:oy,LineBasicMaterial:Gn,Material:Nn};return new t[e]}}class Jd{static decodeText(e){if(console.warn("THREE.LoaderUtils: decodeText() has been deprecated with r165 and will be removed with r175. Use TextDecoder instead."),typeof TextDecoder<"u")return new TextDecoder().decode(e);let t="";for(let n=0,i=e.length;n<i;n++)t+=String.fromCharCode(e[n]);try{return decodeURIComponent(escape(t))}catch{return t}}static extractUrlBase(e){const t=e.lastIndexOf("/");return t===-1?"./":e.slice(0,t+1)}static resolveURL(e,t){return typeof e!="string"||e===""?"":(/^https?:\/\//i.test(t)&&/^\//.test(e)&&(t=t.replace(/(^https?:\/\/[^\/]+).*/i,"$1")),/^(https?:)?\/\//i.test(e)||/^data:.*,.*$/i.test(e)||/^blob:.*$/i.test(e)?e:t+e)}}class zp extends xt{constructor(){super(),this.isInstancedBufferGeometry=!0,this.type="InstancedBufferGeometry",this.instanceCount=1/0}copy(e){return super.copy(e),this.instanceCount=e.instanceCount,this}toJSON(){const e=super.toJSON();return e.instanceCount=this.instanceCount,e.isInstancedBufferGeometry=!0,e}}class Sy extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=new xr(s.manager);l.setPath(s.path),l.setRequestHeader(s.requestHeader),l.setWithCredentials(s.withCredentials),l.load(e,function(c){try{t(s.parse(JSON.parse(c)))}catch(u){i?i(u):console.error(u),s.manager.itemError(e)}},n,i)}parse(e){const t={},n={};function i(g,y){if(t[y]!==void 0)return t[y];const x=g.interleavedBuffers[y],_=s(g,x.buffer),w=To(x.type,_),E=new uh(w,x.stride);return E.uuid=x.uuid,t[y]=E,E}function s(g,y){if(n[y]!==void 0)return n[y];const x=g.arrayBuffers[y],_=new Uint32Array(x).buffer;return n[y]=_,_}const l=e.isInstancedBufferGeometry?new zp:new xt,c=e.data.index;if(c!==void 0){const g=To(c.type,c.array);l.setIndex(new zt(g,1))}const u=e.data.attributes;for(const g in u){const y=u[g];let M;if(y.isInterleavedBufferAttribute){const x=i(e.data,y.data);M=new si(x,y.itemSize,y.offset,y.normalized)}else{const x=To(y.type,y.array),_=y.isInstancedBufferAttribute?Uo:zt;M=new _(x,y.itemSize,y.normalized)}y.name!==void 0&&(M.name=y.name),y.usage!==void 0&&M.setUsage(y.usage),l.setAttribute(g,M)}const h=e.data.morphAttributes;if(h)for(const g in h){const y=h[g],M=[];for(let x=0,_=y.length;x<_;x++){const w=y[x];let E;if(w.isInterleavedBufferAttribute){const T=i(e.data,w.data);E=new si(T,w.itemSize,w.offset,w.normalized)}else{const T=To(w.type,w.array);E=new zt(T,w.itemSize,w.normalized)}w.name!==void 0&&(E.name=w.name),M.push(E)}l.morphAttributes[g]=M}e.data.morphTargetsRelative&&(l.morphTargetsRelative=!0);const p=e.data.groups||e.data.drawcalls||e.data.offsets;if(p!==void 0)for(let g=0,y=p.length;g!==y;++g){const M=p[g];l.addGroup(M.start,M.count,M.materialIndex)}const m=e.data.boundingSphere;if(m!==void 0){const g=new L;m.center!==void 0&&g.fromArray(m.center),l.boundingSphere=new yn(g,m.radius)}return e.name&&(l.name=e.name),e.userData&&(l.userData=e.userData),l}}class QA extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=this.path===""?Jd.extractUrlBase(e):this.path;this.resourcePath=this.resourcePath||l;const c=new xr(this.manager);c.setPath(this.path),c.setRequestHeader(this.requestHeader),c.setWithCredentials(this.withCredentials),c.load(e,function(u){let h=null;try{h=JSON.parse(u)}catch(p){i!==void 0&&i(p),console.error("THREE:ObjectLoader: Can't parse "+e+".",p.message);return}const f=h.metadata;if(f===void 0||f.type===void 0||f.type.toLowerCase()==="geometry"){i!==void 0&&i(new Error("THREE.ObjectLoader: Can't load "+e)),console.error("THREE.ObjectLoader: Can't load "+e);return}s.parse(h,t)},n,i)}async loadAsync(e,t){const n=this,i=this.path===""?Jd.extractUrlBase(e):this.path;this.resourcePath=this.resourcePath||i;const s=new xr(this.manager);s.setPath(this.path),s.setRequestHeader(this.requestHeader),s.setWithCredentials(this.withCredentials);const l=await s.loadAsync(e,t),c=JSON.parse(l),u=c.metadata;if(u===void 0||u.type===void 0||u.type.toLowerCase()==="geometry")throw new Error("THREE.ObjectLoader: Can't load "+e);return await n.parseAsync(c)}parse(e,t){const n=this.parseAnimations(e.animations),i=this.parseShapes(e.shapes),s=this.parseGeometries(e.geometries,i),l=this.parseImages(e.images,function(){t!==void 0&&t(h)}),c=this.parseTextures(e.textures,l),u=this.parseMaterials(e.materials,c),h=this.parseObject(e.object,s,u,c,n),f=this.parseSkeletons(e.skeletons,h);if(this.bindSkeletons(h,f),this.bindLightTargets(h),t!==void 0){let p=!1;for(const m in l)if(l[m].data instanceof HTMLImageElement){p=!0;break}p===!1&&t(h)}return h}async parseAsync(e){const t=this.parseAnimations(e.animations),n=this.parseShapes(e.shapes),i=this.parseGeometries(e.geometries,n),s=await this.parseImagesAsync(e.images),l=this.parseTextures(e.textures,s),c=this.parseMaterials(e.materials,l),u=this.parseObject(e.object,i,c,l,t),h=this.parseSkeletons(e.skeletons,u);return this.bindSkeletons(u,h),this.bindLightTargets(u),u}parseShapes(e){const t={};if(e!==void 0)for(let n=0,i=e.length;n<i;n++){const s=new Rs().fromJSON(e[n]);t[s.uuid]=s}return t}parseSkeletons(e,t){const n={},i={};if(t.traverse(function(s){s.isBone&&(i[s.uuid]=s)}),e!==void 0)for(let s=0,l=e.length;s<l;s++){const c=new hh().fromJSON(e[s],i);n[c.uuid]=c}return n}parseGeometries(e,t){const n={};if(e!==void 0){const i=new Sy;for(let s=0,l=e.length;s<l;s++){let c;const u=e[s];switch(u.type){case"BufferGeometry":case"InstancedBufferGeometry":c=i.parse(u);break;default:u.type in k0?c=k0[u.type].fromJSON(u,t):console.warn(`THREE.ObjectLoader: Unsupported geometry type "${u.type}"`)}c.uuid=u.uuid,u.name!==void 0&&(c.name=u.name),u.userData!==void 0&&(c.userData=u.userData),n[u.uuid]=c}}return n}parseMaterials(e,t){const n={},i={};if(e!==void 0){const s=new bh;s.setTextures(t);for(let l=0,c=e.length;l<c;l++){const u=e[l];n[u.uuid]===void 0&&(n[u.uuid]=s.parse(u)),i[u.uuid]=n[u.uuid]}}return i}parseAnimations(e){const t={};if(e!==void 0)for(let n=0;n<e.length;n++){const i=e[n],s=Za.parse(i);t[s.uuid]=s}return t}parseImages(e,t){const n=this,i={};let s;function l(u){return n.manager.itemStart(u),s.load(u,function(){n.manager.itemEnd(u)},void 0,function(){n.manager.itemError(u),n.manager.itemEnd(u)})}function c(u){if(typeof u=="string"){const h=u,f=/^(\/\/)|([a-z]+:(\/\/)?)/i.test(h)?h:n.resourcePath+h;return l(f)}else return u.data?{data:To(u.type,u.data),width:u.width,height:u.height}:null}if(e!==void 0&&e.length>0){const u=new Fp(t);s=new ja(u),s.setCrossOrigin(this.crossOrigin);for(let h=0,f=e.length;h<f;h++){const p=e[h],m=p.url;if(Array.isArray(m)){const g=[];for(let y=0,M=m.length;y<M;y++){const x=m[y],_=c(x);_!==null&&(_ instanceof HTMLImageElement?g.push(_):g.push(new Zi(_.data,_.width,_.height)))}i[p.uuid]=new Es(g)}else{const g=c(p.url);i[p.uuid]=new Es(g)}}}return i}async parseImagesAsync(e){const t=this,n={};let i;async function s(l){if(typeof l=="string"){const c=l,u=/^(\/\/)|([a-z]+:(\/\/)?)/i.test(c)?c:t.resourcePath+c;return await i.loadAsync(u)}else return l.data?{data:To(l.type,l.data),width:l.width,height:l.height}:null}if(e!==void 0&&e.length>0){i=new ja(this.manager),i.setCrossOrigin(this.crossOrigin);for(let l=0,c=e.length;l<c;l++){const u=e[l],h=u.url;if(Array.isArray(h)){const f=[];for(let p=0,m=h.length;p<m;p++){const g=h[p],y=await s(g);y!==null&&(y instanceof HTMLImageElement?f.push(y):f.push(new Zi(y.data,y.width,y.height)))}n[u.uuid]=new Es(f)}else{const f=await s(u.url);n[u.uuid]=new Es(f)}}}return n}parseTextures(e,t){function n(s,l){return typeof s=="number"?s:(console.warn("THREE.ObjectLoader.parseTexture: Constant should be in numeric form.",s),l[s])}const i={};if(e!==void 0)for(let s=0,l=e.length;s<l;s++){const c=e[s];c.image===void 0&&console.warn('THREE.ObjectLoader: No "image" specified for',c.uuid),t[c.image]===void 0&&console.warn("THREE.ObjectLoader: Undefined image",c.image);const u=t[c.image],h=u.data;let f;Array.isArray(h)?(f=new tl,h.length===6&&(f.needsUpdate=!0)):(h&&h.data?f=new Zi:f=new Kt,h&&(f.needsUpdate=!0)),f.source=u,f.uuid=c.uuid,c.name!==void 0&&(f.name=c.name),c.mapping!==void 0&&(f.mapping=n(c.mapping,$A)),c.channel!==void 0&&(f.channel=c.channel),c.offset!==void 0&&f.offset.fromArray(c.offset),c.repeat!==void 0&&f.repeat.fromArray(c.repeat),c.center!==void 0&&f.center.fromArray(c.center),c.rotation!==void 0&&(f.rotation=c.rotation),c.wrap!==void 0&&(f.wrapS=n(c.wrap[0],W0),f.wrapT=n(c.wrap[1],W0)),c.format!==void 0&&(f.format=c.format),c.internalFormat!==void 0&&(f.internalFormat=c.internalFormat),c.type!==void 0&&(f.type=c.type),c.colorSpace!==void 0&&(f.colorSpace=c.colorSpace),c.minFilter!==void 0&&(f.minFilter=n(c.minFilter,X0)),c.magFilter!==void 0&&(f.magFilter=n(c.magFilter,X0)),c.anisotropy!==void 0&&(f.anisotropy=c.anisotropy),c.flipY!==void 0&&(f.flipY=c.flipY),c.generateMipmaps!==void 0&&(f.generateMipmaps=c.generateMipmaps),c.premultiplyAlpha!==void 0&&(f.premultiplyAlpha=c.premultiplyAlpha),c.unpackAlignment!==void 0&&(f.unpackAlignment=c.unpackAlignment),c.compareFunction!==void 0&&(f.compareFunction=c.compareFunction),c.userData!==void 0&&(f.userData=c.userData),i[c.uuid]=f}return i}parseObject(e,t,n,i,s){let l;function c(m){return t[m]===void 0&&console.warn("THREE.ObjectLoader: Undefined geometry",m),t[m]}function u(m){if(m!==void 0){if(Array.isArray(m)){const g=[];for(let y=0,M=m.length;y<M;y++){const x=m[y];n[x]===void 0&&console.warn("THREE.ObjectLoader: Undefined material",x),g.push(n[x])}return g}return n[m]===void 0&&console.warn("THREE.ObjectLoader: Undefined material",m),n[m]}}function h(m){return i[m]===void 0&&console.warn("THREE.ObjectLoader: Undefined texture",m),i[m]}let f,p;switch(e.type){case"Scene":l=new Mp,e.background!==void 0&&(Number.isInteger(e.background)?l.background=new Be(e.background):l.background=h(e.background)),e.environment!==void 0&&(l.environment=h(e.environment)),e.fog!==void 0&&(e.fog.type==="Fog"?l.fog=new ch(e.fog.color,e.fog.near,e.fog.far):e.fog.type==="FogExp2"&&(l.fog=new lh(e.fog.color,e.fog.density)),e.fog.name!==""&&(l.fog.name=e.fog.name)),e.backgroundBlurriness!==void 0&&(l.backgroundBlurriness=e.backgroundBlurriness),e.backgroundIntensity!==void 0&&(l.backgroundIntensity=e.backgroundIntensity),e.backgroundRotation!==void 0&&l.backgroundRotation.fromArray(e.backgroundRotation),e.environmentIntensity!==void 0&&(l.environmentIntensity=e.environmentIntensity),e.environmentRotation!==void 0&&l.environmentRotation.fromArray(e.environmentRotation);break;case"PerspectiveCamera":l=new tn(e.fov,e.aspect,e.near,e.far),e.focus!==void 0&&(l.focus=e.focus),e.zoom!==void 0&&(l.zoom=e.zoom),e.filmGauge!==void 0&&(l.filmGauge=e.filmGauge),e.filmOffset!==void 0&&(l.filmOffset=e.filmOffset),e.view!==void 0&&(l.view=Object.assign({},e.view));break;case"OrthographicCamera":l=new kr(e.left,e.right,e.top,e.bottom,e.near,e.far),e.zoom!==void 0&&(l.zoom=e.zoom),e.view!==void 0&&(l.view=Object.assign({},e.view));break;case"AmbientLight":l=new vy(e.color,e.intensity);break;case"DirectionalLight":l=new gy(e.color,e.intensity),l.target=e.target||"";break;case"PointLight":l=new my(e.color,e.intensity,e.distance,e.decay);break;case"RectAreaLight":l=new _y(e.color,e.intensity,e.width,e.height);break;case"SpotLight":l=new py(e.color,e.intensity,e.distance,e.angle,e.penumbra,e.decay),l.target=e.target||"";break;case"HemisphereLight":l=new dy(e.color,e.groundColor,e.intensity);break;case"LightProbe":l=new xy().fromJSON(e);break;case"SkinnedMesh":f=c(e.geometry),p=u(e.material),l=new B_(f,p),e.bindMode!==void 0&&(l.bindMode=e.bindMode),e.bindMatrix!==void 0&&l.bindMatrix.fromArray(e.bindMatrix),e.skeleton!==void 0&&(l.skeleton=e.skeleton);break;case"Mesh":f=c(e.geometry),p=u(e.material),l=new nn(f,p);break;case"InstancedMesh":f=c(e.geometry),p=u(e.material);const m=e.count,g=e.instanceMatrix,y=e.instanceColor;l=new z_(f,p,m),l.instanceMatrix=new Uo(new Float32Array(g.array),16),y!==void 0&&(l.instanceColor=new Uo(new Float32Array(y.array),y.itemSize));break;case"BatchedMesh":f=c(e.geometry),p=u(e.material),l=new k_(e.maxInstanceCount,e.maxVertexCount,e.maxIndexCount,p),l.geometry=f,l.perObjectFrustumCulled=e.perObjectFrustumCulled,l.sortObjects=e.sortObjects,l._drawRanges=e.drawRanges,l._reservedRanges=e.reservedRanges,l._visibility=e.visibility,l._active=e.active,l._bounds=e.bounds.map(M=>{const x=new _n;x.min.fromArray(M.boxMin),x.max.fromArray(M.boxMax);const _=new yn;return _.radius=M.sphereRadius,_.center.fromArray(M.sphereCenter),{boxInitialized:M.boxInitialized,box:x,sphereInitialized:M.sphereInitialized,sphere:_}}),l._maxInstanceCount=e.maxInstanceCount,l._maxVertexCount=e.maxVertexCount,l._maxIndexCount=e.maxIndexCount,l._geometryInitialized=e.geometryInitialized,l._geometryCount=e.geometryCount,l._matricesTexture=h(e.matricesTexture.uuid),e.colorsTexture!==void 0&&(l._colorsTexture=h(e.colorsTexture.uuid));break;case"LOD":l=new F_;break;case"Line":l=new Vr(c(e.geometry),u(e.material));break;case"LineLoop":l=new H_(c(e.geometry),u(e.material));break;case"LineSegments":l=new Ki(c(e.geometry),u(e.material));break;case"PointCloud":case"Points":l=new V_(c(e.geometry),u(e.material));break;case"Sprite":l=new O_(u(e.material));break;case"Group":l=new bo;break;case"Bone":l=new wp;break;default:l=new Dt}if(l.uuid=e.uuid,e.name!==void 0&&(l.name=e.name),e.matrix!==void 0?(l.matrix.fromArray(e.matrix),e.matrixAutoUpdate!==void 0&&(l.matrixAutoUpdate=e.matrixAutoUpdate),l.matrixAutoUpdate&&l.matrix.decompose(l.position,l.quaternion,l.scale)):(e.position!==void 0&&l.position.fromArray(e.position),e.rotation!==void 0&&l.rotation.fromArray(e.rotation),e.quaternion!==void 0&&l.quaternion.fromArray(e.quaternion),e.scale!==void 0&&l.scale.fromArray(e.scale)),e.up!==void 0&&l.up.fromArray(e.up),e.castShadow!==void 0&&(l.castShadow=e.castShadow),e.receiveShadow!==void 0&&(l.receiveShadow=e.receiveShadow),e.shadow&&(e.shadow.intensity!==void 0&&(l.shadow.intensity=e.shadow.intensity),e.shadow.bias!==void 0&&(l.shadow.bias=e.shadow.bias),e.shadow.normalBias!==void 0&&(l.shadow.normalBias=e.shadow.normalBias),e.shadow.radius!==void 0&&(l.shadow.radius=e.shadow.radius),e.shadow.mapSize!==void 0&&l.shadow.mapSize.fromArray(e.shadow.mapSize),e.shadow.camera!==void 0&&(l.shadow.camera=this.parseObject(e.shadow.camera))),e.visible!==void 0&&(l.visible=e.visible),e.frustumCulled!==void 0&&(l.frustumCulled=e.frustumCulled),e.renderOrder!==void 0&&(l.renderOrder=e.renderOrder),e.userData!==void 0&&(l.userData=e.userData),e.layers!==void 0&&(l.layers.mask=e.layers),e.children!==void 0){const m=e.children;for(let g=0;g<m.length;g++)l.add(this.parseObject(m[g],t,n,i,s))}if(e.animations!==void 0){const m=e.animations;for(let g=0;g<m.length;g++){const y=m[g];l.animations.push(s[y])}}if(e.type==="LOD"){e.autoUpdate!==void 0&&(l.autoUpdate=e.autoUpdate);const m=e.levels;for(let g=0;g<m.length;g++){const y=m[g],M=l.getObjectByProperty("uuid",y.object);M!==void 0&&l.addLevel(M,y.distance,y.hysteresis)}}return l}bindSkeletons(e,t){Object.keys(t).length!==0&&e.traverse(function(n){if(n.isSkinnedMesh===!0&&n.skeleton!==void 0){const i=t[n.skeleton];i===void 0?console.warn("THREE.ObjectLoader: No skeleton found with UUID:",n.skeleton):n.bind(i,n.bindMatrix)}})}bindLightTargets(e){e.traverse(function(t){if(t.isDirectionalLight||t.isSpotLight){const n=t.target,i=e.getObjectByProperty("uuid",n);i!==void 0?t.target=i:t.target=new Dt}})}}const $A={UVMapping:Qu,CubeReflectionMapping:_r,CubeRefractionMapping:Hr,EquirectangularReflectionMapping:Da,EquirectangularRefractionMapping:Ua,CubeUVReflectionMapping:Oo},W0={RepeatWrapping:Na,ClampToEdgeWrapping:vi,MirroredRepeatWrapping:Oa},X0={NearestFilter:wn,NearestMipmapNearestFilter:np,NearestMipmapLinearFilter:wo,LinearFilter:cn,LinearMipmapNearestFilter:wa,LinearMipmapLinearFilter:Xi};class eb extends Qn{constructor(e){super(e),this.isImageBitmapLoader=!0,typeof createImageBitmap>"u"&&console.warn("THREE.ImageBitmapLoader: createImageBitmap() not supported."),typeof fetch>"u"&&console.warn("THREE.ImageBitmapLoader: fetch() not supported."),this.options={premultiplyAlpha:"none"}}setOptions(e){return this.options=e,this}load(e,t,n,i){e===void 0&&(e=""),this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);const s=this,l=pr.get(e);if(l!==void 0){if(s.manager.itemStart(e),l.then){l.then(h=>{t&&t(h),s.manager.itemEnd(e)}).catch(h=>{i&&i(h)});return}return setTimeout(function(){t&&t(l),s.manager.itemEnd(e)},0),l}const c={};c.credentials=this.crossOrigin==="anonymous"?"same-origin":"include",c.headers=this.requestHeader;const u=fetch(e,c).then(function(h){return h.blob()}).then(function(h){return createImageBitmap(h,Object.assign(s.options,{colorSpaceConversion:"none"}))}).then(function(h){return pr.add(e,h),t&&t(h),s.manager.itemEnd(e),h}).catch(function(h){i&&i(h),pr.remove(e),s.manager.itemError(e),s.manager.itemEnd(e)});pr.add(e,u),s.manager.itemStart(e)}}let qc;class kp{static getContext(){return qc===void 0&&(qc=new(window.AudioContext||window.webkitAudioContext)),qc}static setContext(e){qc=e}}class tb extends Qn{constructor(e){super(e)}load(e,t,n,i){const s=this,l=new xr(this.manager);l.setResponseType("arraybuffer"),l.setPath(this.path),l.setRequestHeader(this.requestHeader),l.setWithCredentials(this.withCredentials),l.load(e,function(u){try{const h=u.slice(0);kp.getContext().decodeAudioData(h,function(p){t(p)}).catch(c)}catch(h){c(h)}},n,i);function c(u){i?i(u):console.error(u),s.manager.itemError(e)}}}const Y0=new ut,q0=new ut,hs=new ut;class nb{constructor(){this.type="StereoCamera",this.aspect=1,this.eyeSep=.064,this.cameraL=new tn,this.cameraL.layers.enable(1),this.cameraL.matrixAutoUpdate=!1,this.cameraR=new tn,this.cameraR.layers.enable(2),this.cameraR.matrixAutoUpdate=!1,this._cache={focus:null,fov:null,aspect:null,near:null,far:null,zoom:null,eyeSep:null}}update(e){const t=this._cache;if(t.focus!==e.focus||t.fov!==e.fov||t.aspect!==e.aspect*this.aspect||t.near!==e.near||t.far!==e.far||t.zoom!==e.zoom||t.eyeSep!==this.eyeSep){t.focus=e.focus,t.fov=e.fov,t.aspect=e.aspect*this.aspect,t.near=e.near,t.far=e.far,t.zoom=e.zoom,t.eyeSep=this.eyeSep,hs.copy(e.projectionMatrix);const i=t.eyeSep/2,s=i*t.near/t.focus,l=t.near*Math.tan(bs*t.fov*.5)/t.zoom;let c,u;q0.elements[12]=-i,Y0.elements[12]=i,c=-l*t.aspect+s,u=l*t.aspect+s,hs.elements[0]=2*t.near/(u-c),hs.elements[8]=(u+c)/(u-c),this.cameraL.projectionMatrix.copy(hs),c=-l*t.aspect-s,u=l*t.aspect-s,hs.elements[0]=2*t.near/(u-c),hs.elements[8]=(u+c)/(u-c),this.cameraR.projectionMatrix.copy(hs)}this.cameraL.matrixWorld.copy(e.matrixWorld).multiply(q0),this.cameraR.matrixWorld.copy(e.matrixWorld).multiply(Y0)}}class Hp{constructor(e=!0){this.autoStart=e,this.startTime=0,this.oldTime=0,this.elapsedTime=0,this.running=!1}start(){this.startTime=Z0(),this.oldTime=this.startTime,this.elapsedTime=0,this.running=!0}stop(){this.getElapsedTime(),this.running=!1,this.autoStart=!1}getElapsedTime(){return this.getDelta(),this.elapsedTime}getDelta(){let e=0;if(this.autoStart&&!this.running)return this.start(),0;if(this.running){const t=Z0();e=(t-this.oldTime)/1e3,this.oldTime=t,this.elapsedTime+=e}return e}}function Z0(){return performance.now()}const fs=new L,j0=new Un,ib=new L,ds=new L;class rb extends Dt{constructor(){super(),this.type="AudioListener",this.context=kp.getContext(),this.gain=this.context.createGain(),this.gain.connect(this.context.destination),this.filter=null,this.timeDelta=0,this._clock=new Hp}getInput(){return this.gain}removeFilter(){return this.filter!==null&&(this.gain.disconnect(this.filter),this.filter.disconnect(this.context.destination),this.gain.connect(this.context.destination),this.filter=null),this}getFilter(){return this.filter}setFilter(e){return this.filter!==null?(this.gain.disconnect(this.filter),this.filter.disconnect(this.context.destination)):this.gain.disconnect(this.context.destination),this.filter=e,this.gain.connect(this.filter),this.filter.connect(this.context.destination),this}getMasterVolume(){return this.gain.gain.value}setMasterVolume(e){return this.gain.gain.setTargetAtTime(e,this.context.currentTime,.01),this}updateMatrixWorld(e){super.updateMatrixWorld(e);const t=this.context.listener,n=this.up;if(this.timeDelta=this._clock.getDelta(),this.matrixWorld.decompose(fs,j0,ib),ds.set(0,0,-1).applyQuaternion(j0),t.positionX){const i=this.context.currentTime+this.timeDelta;t.positionX.linearRampToValueAtTime(fs.x,i),t.positionY.linearRampToValueAtTime(fs.y,i),t.positionZ.linearRampToValueAtTime(fs.z,i),t.forwardX.linearRampToValueAtTime(ds.x,i),t.forwardY.linearRampToValueAtTime(ds.y,i),t.forwardZ.linearRampToValueAtTime(ds.z,i),t.upX.linearRampToValueAtTime(n.x,i),t.upY.linearRampToValueAtTime(n.y,i),t.upZ.linearRampToValueAtTime(n.z,i)}else t.setPosition(fs.x,fs.y,fs.z),t.setOrientation(ds.x,ds.y,ds.z,n.x,n.y,n.z)}}class My extends Dt{constructor(e){super(),this.type="Audio",this.listener=e,this.context=e.context,this.gain=this.context.createGain(),this.gain.connect(e.getInput()),this.autoplay=!1,this.buffer=null,this.detune=0,this.loop=!1,this.loopStart=0,this.loopEnd=0,this.offset=0,this.duration=void 0,this.playbackRate=1,this.isPlaying=!1,this.hasPlaybackControl=!0,this.source=null,this.sourceType="empty",this._startedAt=0,this._progress=0,this._connected=!1,this.filters=[]}getOutput(){return this.gain}setNodeSource(e){return this.hasPlaybackControl=!1,this.sourceType="audioNode",this.source=e,this.connect(),this}setMediaElementSource(e){return this.hasPlaybackControl=!1,this.sourceType="mediaNode",this.source=this.context.createMediaElementSource(e),this.connect(),this}setMediaStreamSource(e){return this.hasPlaybackControl=!1,this.sourceType="mediaStreamNode",this.source=this.context.createMediaStreamSource(e),this.connect(),this}setBuffer(e){return this.buffer=e,this.sourceType="buffer",this.autoplay&&this.play(),this}play(e=0){if(this.isPlaying===!0){console.warn("THREE.Audio: Audio is already playing.");return}if(this.hasPlaybackControl===!1){console.warn("THREE.Audio: this Audio has no playback control.");return}this._startedAt=this.context.currentTime+e;const t=this.context.createBufferSource();return t.buffer=this.buffer,t.loop=this.loop,t.loopStart=this.loopStart,t.loopEnd=this.loopEnd,t.onended=this.onEnded.bind(this),t.start(this._startedAt,this._progress+this.offset,this.duration),this.isPlaying=!0,this.source=t,this.setDetune(this.detune),this.setPlaybackRate(this.playbackRate),this.connect()}pause(){if(this.hasPlaybackControl===!1){console.warn("THREE.Audio: this Audio has no playback control.");return}return this.isPlaying===!0&&(this._progress+=Math.max(this.context.currentTime-this._startedAt,0)*this.playbackRate,this.loop===!0&&(this._progress=this._progress%(this.duration||this.buffer.duration)),this.source.stop(),this.source.onended=null,this.isPlaying=!1),this}stop(e=0){if(this.hasPlaybackControl===!1){console.warn("THREE.Audio: this Audio has no playback control.");return}return this._progress=0,this.source!==null&&(this.source.stop(this.context.currentTime+e),this.source.onended=null),this.isPlaying=!1,this}connect(){if(this.filters.length>0){this.source.connect(this.filters[0]);for(let e=1,t=this.filters.length;e<t;e++)this.filters[e-1].connect(this.filters[e]);this.filters[this.filters.length-1].connect(this.getOutput())}else this.source.connect(this.getOutput());return this._connected=!0,this}disconnect(){if(this._connected!==!1){if(this.filters.length>0){this.source.disconnect(this.filters[0]);for(let e=1,t=this.filters.length;e<t;e++)this.filters[e-1].disconnect(this.filters[e]);this.filters[this.filters.length-1].disconnect(this.getOutput())}else this.source.disconnect(this.getOutput());return this._connected=!1,this}}getFilters(){return this.filters}setFilters(e){return e||(e=[]),this._connected===!0?(this.disconnect(),this.filters=e.slice(),this.connect()):this.filters=e.slice(),this}setDetune(e){return this.detune=e,this.isPlaying===!0&&this.source.detune!==void 0&&this.source.detune.setTargetAtTime(this.detune,this.context.currentTime,.01),this}getDetune(){return this.detune}getFilter(){return this.getFilters()[0]}setFilter(e){return this.setFilters(e?[e]:[])}setPlaybackRate(e){if(this.hasPlaybackControl===!1){console.warn("THREE.Audio: this Audio has no playback control.");return}return this.playbackRate=e,this.isPlaying===!0&&this.source.playbackRate.setTargetAtTime(this.playbackRate,this.context.currentTime,.01),this}getPlaybackRate(){return this.playbackRate}onEnded(){this.isPlaying=!1}getLoop(){return this.hasPlaybackControl===!1?(console.warn("THREE.Audio: this Audio has no playback control."),!1):this.loop}setLoop(e){if(this.hasPlaybackControl===!1){console.warn("THREE.Audio: this Audio has no playback control.");return}return this.loop=e,this.isPlaying===!0&&(this.source.loop=this.loop),this}setLoopStart(e){return this.loopStart=e,this}setLoopEnd(e){return this.loopEnd=e,this}getVolume(){return this.gain.gain.value}setVolume(e){return this.gain.gain.setTargetAtTime(e,this.context.currentTime,.01),this}}const ps=new L,J0=new Un,sb=new L,ms=new L;class ob extends My{constructor(e){super(e),this.panner=this.context.createPanner(),this.panner.panningModel="HRTF",this.panner.connect(this.gain)}connect(){super.connect(),this.panner.connect(this.gain)}disconnect(){super.disconnect(),this.panner.disconnect(this.gain)}getOutput(){return this.panner}getRefDistance(){return this.panner.refDistance}setRefDistance(e){return this.panner.refDistance=e,this}getRolloffFactor(){return this.panner.rolloffFactor}setRolloffFactor(e){return this.panner.rolloffFactor=e,this}getDistanceModel(){return this.panner.distanceModel}setDistanceModel(e){return this.panner.distanceModel=e,this}getMaxDistance(){return this.panner.maxDistance}setMaxDistance(e){return this.panner.maxDistance=e,this}setDirectionalCone(e,t,n){return this.panner.coneInnerAngle=e,this.panner.coneOuterAngle=t,this.panner.coneOuterGain=n,this}updateMatrixWorld(e){if(super.updateMatrixWorld(e),this.hasPlaybackControl===!0&&this.isPlaying===!1)return;this.matrixWorld.decompose(ps,J0,sb),ms.set(0,0,1).applyQuaternion(J0);const t=this.panner;if(t.positionX){const n=this.context.currentTime+this.listener.timeDelta;t.positionX.linearRampToValueAtTime(ps.x,n),t.positionY.linearRampToValueAtTime(ps.y,n),t.positionZ.linearRampToValueAtTime(ps.z,n),t.orientationX.linearRampToValueAtTime(ms.x,n),t.orientationY.linearRampToValueAtTime(ms.y,n),t.orientationZ.linearRampToValueAtTime(ms.z,n)}else t.setPosition(ps.x,ps.y,ps.z),t.setOrientation(ms.x,ms.y,ms.z)}}class ab{constructor(e,t=2048){this.analyser=e.context.createAnalyser(),this.analyser.fftSize=t,this.data=new Uint8Array(this.analyser.frequencyBinCount),e.getOutput().connect(this.analyser)}getFrequencyData(){return this.analyser.getByteFrequencyData(this.data),this.data}getAverageFrequency(){let e=0;const t=this.getFrequencyData();for(let n=0;n<t.length;n++)e+=t[n];return e/t.length}}class Ey{constructor(e,t,n){this.binding=e,this.valueSize=n;let i,s,l;switch(t){case"quaternion":i=this._slerp,s=this._slerpAdditive,l=this._setAdditiveIdentityQuaternion,this.buffer=new Float64Array(n*6),this._workIndex=5;break;case"string":case"bool":i=this._select,s=this._select,l=this._setAdditiveIdentityOther,this.buffer=new Array(n*5);break;default:i=this._lerp,s=this._lerpAdditive,l=this._setAdditiveIdentityNumeric,this.buffer=new Float64Array(n*5)}this._mixBufferRegion=i,this._mixBufferRegionAdditive=s,this._setIdentity=l,this._origIndex=3,this._addIndex=4,this.cumulativeWeight=0,this.cumulativeWeightAdditive=0,this.useCount=0,this.referenceCount=0}accumulate(e,t){const n=this.buffer,i=this.valueSize,s=e*i+i;let l=this.cumulativeWeight;if(l===0){for(let c=0;c!==i;++c)n[s+c]=n[c];l=t}else{l+=t;const c=t/l;this._mixBufferRegion(n,s,0,c,i)}this.cumulativeWeight=l}accumulateAdditive(e){const t=this.buffer,n=this.valueSize,i=n*this._addIndex;this.cumulativeWeightAdditive===0&&this._setIdentity(),this._mixBufferRegionAdditive(t,i,0,e,n),this.cumulativeWeightAdditive+=e}apply(e){const t=this.valueSize,n=this.buffer,i=e*t+t,s=this.cumulativeWeight,l=this.cumulativeWeightAdditive,c=this.binding;if(this.cumulativeWeight=0,this.cumulativeWeightAdditive=0,s<1){const u=t*this._origIndex;this._mixBufferRegion(n,i,u,1-s,t)}l>0&&this._mixBufferRegionAdditive(n,i,this._addIndex*t,1,t);for(let u=t,h=t+t;u!==h;++u)if(n[u]!==n[u+t]){c.setValue(n,i);break}}saveOriginalState(){const e=this.binding,t=this.buffer,n=this.valueSize,i=n*this._origIndex;e.getValue(t,i);for(let s=n,l=i;s!==l;++s)t[s]=t[i+s%n];this._setIdentity(),this.cumulativeWeight=0,this.cumulativeWeightAdditive=0}restoreOriginalState(){const e=this.valueSize*3;this.binding.setValue(this.buffer,e)}_setAdditiveIdentityNumeric(){const e=this._addIndex*this.valueSize,t=e+this.valueSize;for(let n=e;n<t;n++)this.buffer[n]=0}_setAdditiveIdentityQuaternion(){this._setAdditiveIdentityNumeric(),this.buffer[this._addIndex*this.valueSize+3]=1}_setAdditiveIdentityOther(){const e=this._origIndex*this.valueSize,t=this._addIndex*this.valueSize;for(let n=0;n<this.valueSize;n++)this.buffer[t+n]=this.buffer[e+n]}_select(e,t,n,i,s){if(i>=.5)for(let l=0;l!==s;++l)e[t+l]=e[n+l]}_slerp(e,t,n,i){Un.slerpFlat(e,t,e,t,e,n,i)}_slerpAdditive(e,t,n,i,s){const l=this._workIndex*s;Un.multiplyQuaternionsFlat(e,l,e,t,e,n),Un.slerpFlat(e,t,e,t,e,l,i)}_lerp(e,t,n,i,s){const l=1-i;for(let c=0;c!==s;++c){const u=t+c;e[u]=e[u]*l+e[n+c]*i}}_lerpAdditive(e,t,n,i,s){for(let l=0;l!==s;++l){const c=t+l;e[c]=e[c]+e[n+l]*i}}}const Vp="\\[\\]\\.:\\/",lb=new RegExp("["+Vp+"]","g"),Gp="[^"+Vp+"]",cb="[^"+Vp.replace("\\.","")+"]",ub=/((?:WC+[\/:])*)/.source.replace("WC",Gp),hb=/(WCOD+)?/.source.replace("WCOD",cb),fb=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",Gp),db=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",Gp),pb=new RegExp("^"+ub+hb+fb+db+"$"),mb=["material","materials","bones","map"];class gb{constructor(e,t,n){const i=n||Lt.parseTrackName(t);this._targetGroup=e,this._bindings=e.subscribe_(t,i)}getValue(e,t){this.bind();const n=this._targetGroup.nCachedObjects_,i=this._bindings[n];i!==void 0&&i.getValue(e,t)}setValue(e,t){const n=this._bindings;for(let i=this._targetGroup.nCachedObjects_,s=n.length;i!==s;++i)n[i].setValue(e,t)}bind(){const e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,n=e.length;t!==n;++t)e[t].bind()}unbind(){const e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,n=e.length;t!==n;++t)e[t].unbind()}}class Lt{constructor(e,t,n){this.path=t,this.parsedPath=n||Lt.parseTrackName(t),this.node=Lt.findNode(e,this.parsedPath.nodeName),this.rootNode=e,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(e,t,n){return e&&e.isAnimationObjectGroup?new Lt.Composite(e,t,n):new Lt(e,t,n)}static sanitizeNodeName(e){return e.replace(/\s/g,"_").replace(lb,"")}static parseTrackName(e){const t=pb.exec(e);if(t===null)throw new Error("PropertyBinding: Cannot parse trackName: "+e);const n={nodeName:t[2],objectName:t[3],objectIndex:t[4],propertyName:t[5],propertyIndex:t[6]},i=n.nodeName&&n.nodeName.lastIndexOf(".");if(i!==void 0&&i!==-1){const s=n.nodeName.substring(i+1);mb.indexOf(s)!==-1&&(n.nodeName=n.nodeName.substring(0,i),n.objectName=s)}if(n.propertyName===null||n.propertyName.length===0)throw new Error("PropertyBinding: can not parse propertyName from trackName: "+e);return n}static findNode(e,t){if(t===void 0||t===""||t==="."||t===-1||t===e.name||t===e.uuid)return e;if(e.skeleton){const n=e.skeleton.getBoneByName(t);if(n!==void 0)return n}if(e.children){const n=function(s){for(let l=0;l<s.length;l++){const c=s[l];if(c.name===t||c.uuid===t)return c;const u=n(c.children);if(u)return u}return null},i=n(e.children);if(i)return i}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(e,t){e[t]=this.targetObject[this.propertyName]}_getValue_array(e,t){const n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)e[t++]=n[i]}_getValue_arrayElement(e,t){e[t]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(e,t){this.resolvedProperty.toArray(e,t)}_setValue_direct(e,t){this.targetObject[this.propertyName]=e[t]}_setValue_direct_setNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(e,t){const n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=e[t++]}_setValue_array_setNeedsUpdate(e,t){const n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=e[t++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(e,t){const n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=e[t++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(e,t){this.resolvedProperty[this.propertyIndex]=e[t]}_setValue_arrayElement_setNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(e,t){this.resolvedProperty.fromArray(e,t)}_setValue_fromArray_setNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(e,t){this.bind(),this.getValue(e,t)}_setValue_unbound(e,t){this.bind(),this.setValue(e,t)}bind(){let e=this.node;const t=this.parsedPath,n=t.objectName,i=t.propertyName;let s=t.propertyIndex;if(e||(e=Lt.findNode(this.rootNode,t.nodeName),this.node=e),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!e){console.warn("THREE.PropertyBinding: No target node found for track: "+this.path+".");return}if(n){let h=t.objectIndex;switch(n){case"materials":if(!e.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.materials){console.error("THREE.PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}e=e.material.materials;break;case"bones":if(!e.skeleton){console.error("THREE.PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}e=e.skeleton.bones;for(let f=0;f<e.length;f++)if(e[f].name===h){h=f;break}break;case"map":if("map"in e){e=e.map;break}if(!e.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.map){console.error("THREE.PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}e=e.material.map;break;default:if(e[n]===void 0){console.error("THREE.PropertyBinding: Can not bind to objectName of node undefined.",this);return}e=e[n]}if(h!==void 0){if(e[h]===void 0){console.error("THREE.PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,e);return}e=e[h]}}const l=e[i];if(l===void 0){const h=t.nodeName;console.error("THREE.PropertyBinding: Trying to update property for track: "+h+"."+i+" but it wasn't found.",e);return}let c=this.Versioning.None;this.targetObject=e,e.needsUpdate!==void 0?c=this.Versioning.NeedsUpdate:e.matrixWorldNeedsUpdate!==void 0&&(c=this.Versioning.MatrixWorldNeedsUpdate);let u=this.BindingType.Direct;if(s!==void 0){if(i==="morphTargetInfluences"){if(!e.geometry){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!e.geometry.morphAttributes){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}e.morphTargetDictionary[s]!==void 0&&(s=e.morphTargetDictionary[s])}u=this.BindingType.ArrayElement,this.resolvedProperty=l,this.propertyIndex=s}else l.fromArray!==void 0&&l.toArray!==void 0?(u=this.BindingType.HasFromToArray,this.resolvedProperty=l):Array.isArray(l)?(u=this.BindingType.EntireArray,this.resolvedProperty=l):this.propertyName=i;this.getValue=this.GetterByBindingType[u],this.setValue=this.SetterByBindingTypeAndVersioning[u][c]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}}Lt.Composite=gb;Lt.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};Lt.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};Lt.prototype.GetterByBindingType=[Lt.prototype._getValue_direct,Lt.prototype._getValue_array,Lt.prototype._getValue_arrayElement,Lt.prototype._getValue_toArray];Lt.prototype.SetterByBindingTypeAndVersioning=[[Lt.prototype._setValue_direct,Lt.prototype._setValue_direct_setNeedsUpdate,Lt.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[Lt.prototype._setValue_array,Lt.prototype._setValue_array_setNeedsUpdate,Lt.prototype._setValue_array_setMatrixWorldNeedsUpdate],[Lt.prototype._setValue_arrayElement,Lt.prototype._setValue_arrayElement_setNeedsUpdate,Lt.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[Lt.prototype._setValue_fromArray,Lt.prototype._setValue_fromArray_setNeedsUpdate,Lt.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];class vb{constructor(){this.isAnimationObjectGroup=!0,this.uuid=oi(),this._objects=Array.prototype.slice.call(arguments),this.nCachedObjects_=0;const e={};this._indicesByUUID=e;for(let n=0,i=arguments.length;n!==i;++n)e[arguments[n].uuid]=n;this._paths=[],this._parsedPaths=[],this._bindings=[],this._bindingsIndicesByPath={};const t=this;this.stats={objects:{get total(){return t._objects.length},get inUse(){return this.total-t.nCachedObjects_}},get bindingsPerObject(){return t._bindings.length}}}add(){const e=this._objects,t=this._indicesByUUID,n=this._paths,i=this._parsedPaths,s=this._bindings,l=s.length;let c,u=e.length,h=this.nCachedObjects_;for(let f=0,p=arguments.length;f!==p;++f){const m=arguments[f],g=m.uuid;let y=t[g];if(y===void 0){y=u++,t[g]=y,e.push(m);for(let M=0,x=l;M!==x;++M)s[M].push(new Lt(m,n[M],i[M]))}else if(y<h){c=e[y];const M=--h,x=e[M];t[x.uuid]=y,e[y]=x,t[g]=M,e[M]=m;for(let _=0,w=l;_!==w;++_){const E=s[_],T=E[M];let U=E[y];E[y]=T,U===void 0&&(U=new Lt(m,n[_],i[_])),E[M]=U}}else e[y]!==c&&console.error("THREE.AnimationObjectGroup: Different objects with the same UUID detected. Clean the caches or recreate your infrastructure when reloading scenes.")}this.nCachedObjects_=h}remove(){const e=this._objects,t=this._indicesByUUID,n=this._bindings,i=n.length;let s=this.nCachedObjects_;for(let l=0,c=arguments.length;l!==c;++l){const u=arguments[l],h=u.uuid,f=t[h];if(f!==void 0&&f>=s){const p=s++,m=e[p];t[m.uuid]=f,e[f]=m,t[h]=p,e[p]=u;for(let g=0,y=i;g!==y;++g){const M=n[g],x=M[p],_=M[f];M[f]=x,M[p]=_}}}this.nCachedObjects_=s}uncache(){const e=this._objects,t=this._indicesByUUID,n=this._bindings,i=n.length;let s=this.nCachedObjects_,l=e.length;for(let c=0,u=arguments.length;c!==u;++c){const h=arguments[c],f=h.uuid,p=t[f];if(p!==void 0)if(delete t[f],p<s){const m=--s,g=e[m],y=--l,M=e[y];t[g.uuid]=p,e[p]=g,t[M.uuid]=m,e[m]=M,e.pop();for(let x=0,_=i;x!==_;++x){const w=n[x],E=w[m],T=w[y];w[p]=E,w[m]=T,w.pop()}}else{const m=--l,g=e[m];m>0&&(t[g.uuid]=p),e[p]=g,e.pop();for(let y=0,M=i;y!==M;++y){const x=n[y];x[p]=x[m],x.pop()}}}this.nCachedObjects_=s}subscribe_(e,t){const n=this._bindingsIndicesByPath;let i=n[e];const s=this._bindings;if(i!==void 0)return s[i];const l=this._paths,c=this._parsedPaths,u=this._objects,h=u.length,f=this.nCachedObjects_,p=new Array(h);i=s.length,n[e]=i,l.push(e),c.push(t),s.push(p);for(let m=f,g=u.length;m!==g;++m){const y=u[m];p[m]=new Lt(y,e,t)}return p}unsubscribe_(e){const t=this._bindingsIndicesByPath,n=t[e];if(n!==void 0){const i=this._paths,s=this._parsedPaths,l=this._bindings,c=l.length-1,u=l[c],h=e[c];t[h]=n,l[n]=u,l.pop(),s[n]=s[c],s.pop(),i[n]=i[c],i.pop()}}}class wy{constructor(e,t,n=null,i=t.blendMode){this._mixer=e,this._clip=t,this._localRoot=n,this.blendMode=i;const s=t.tracks,l=s.length,c=new Array(l),u={endingStart:Ss,endingEnd:Ss};for(let h=0;h!==l;++h){const f=s[h].createInterpolant(null);c[h]=f,f.settings=u}this._interpolantSettings=u,this._interpolants=c,this._propertyBindings=new Array(l),this._cacheIndex=null,this._byClipCacheIndex=null,this._timeScaleInterpolant=null,this._weightInterpolant=null,this.loop=o_,this._loopCount=-1,this._startTime=null,this.time=0,this.timeScale=1,this._effectiveTimeScale=1,this.weight=1,this._effectiveWeight=1,this.repetitions=1/0,this.paused=!1,this.enabled=!0,this.clampWhenFinished=!1,this.zeroSlopeAtStart=!0,this.zeroSlopeAtEnd=!0}play(){return this._mixer._activateAction(this),this}stop(){return this._mixer._deactivateAction(this),this.reset()}reset(){return this.paused=!1,this.enabled=!0,this.time=0,this._loopCount=-1,this._startTime=null,this.stopFading().stopWarping()}isRunning(){return this.enabled&&!this.paused&&this.timeScale!==0&&this._startTime===null&&this._mixer._isActiveAction(this)}isScheduled(){return this._mixer._isActiveAction(this)}startAt(e){return this._startTime=e,this}setLoop(e,t){return this.loop=e,this.repetitions=t,this}setEffectiveWeight(e){return this.weight=e,this._effectiveWeight=this.enabled?e:0,this.stopFading()}getEffectiveWeight(){return this._effectiveWeight}fadeIn(e){return this._scheduleFading(e,0,1)}fadeOut(e){return this._scheduleFading(e,1,0)}crossFadeFrom(e,t,n){if(e.fadeOut(t),this.fadeIn(t),n){const i=this._clip.duration,s=e._clip.duration,l=s/i,c=i/s;e.warp(1,l,t),this.warp(c,1,t)}return this}crossFadeTo(e,t,n){return e.crossFadeFrom(this,t,n)}stopFading(){const e=this._weightInterpolant;return e!==null&&(this._weightInterpolant=null,this._mixer._takeBackControlInterpolant(e)),this}setEffectiveTimeScale(e){return this.timeScale=e,this._effectiveTimeScale=this.paused?0:e,this.stopWarping()}getEffectiveTimeScale(){return this._effectiveTimeScale}setDuration(e){return this.timeScale=this._clip.duration/e,this.stopWarping()}syncWith(e){return this.time=e.time,this.timeScale=e.timeScale,this.stopWarping()}halt(e){return this.warp(this._effectiveTimeScale,0,e)}warp(e,t,n){const i=this._mixer,s=i.time,l=this.timeScale;let c=this._timeScaleInterpolant;c===null&&(c=i._lendControlInterpolant(),this._timeScaleInterpolant=c);const u=c.parameterPositions,h=c.sampleValues;return u[0]=s,u[1]=s+n,h[0]=e/l,h[1]=t/l,this}stopWarping(){const e=this._timeScaleInterpolant;return e!==null&&(this._timeScaleInterpolant=null,this._mixer._takeBackControlInterpolant(e)),this}getMixer(){return this._mixer}getClip(){return this._clip}getRoot(){return this._localRoot||this._mixer._root}_update(e,t,n,i){if(!this.enabled){this._updateWeight(e);return}const s=this._startTime;if(s!==null){const u=(e-s)*n;u<0||n===0?t=0:(this._startTime=null,t=n*u)}t*=this._updateTimeScale(e);const l=this._updateTime(t),c=this._updateWeight(e);if(c>0){const u=this._interpolants,h=this._propertyBindings;switch(this.blendMode){case fp:for(let f=0,p=u.length;f!==p;++f)u[f].evaluate(l),h[f].accumulateAdditive(c);break;case sh:default:for(let f=0,p=u.length;f!==p;++f)u[f].evaluate(l),h[f].accumulate(i,c)}}}_updateWeight(e){let t=0;if(this.enabled){t=this.weight;const n=this._weightInterpolant;if(n!==null){const i=n.evaluate(e)[0];t*=i,e>n.parameterPositions[1]&&(this.stopFading(),i===0&&(this.enabled=!1))}}return this._effectiveWeight=t,t}_updateTimeScale(e){let t=0;if(!this.paused){t=this.timeScale;const n=this._timeScaleInterpolant;if(n!==null){const i=n.evaluate(e)[0];t*=i,e>n.parameterPositions[1]&&(this.stopWarping(),t===0?this.paused=!0:this.timeScale=t)}}return this._effectiveTimeScale=t,t}_updateTime(e){const t=this._clip.duration,n=this.loop;let i=this.time+e,s=this._loopCount;const l=n===a_;if(e===0)return s===-1?i:l&&(s&1)===1?t-i:i;if(n===s_){s===-1&&(this._loopCount=0,this._setEndings(!0,!0,!1));e:{if(i>=t)i=t;else if(i<0)i=0;else{this.time=i;break e}this.clampWhenFinished?this.paused=!0:this.enabled=!1,this.time=i,this._mixer.dispatchEvent({type:"finished",action:this,direction:e<0?-1:1})}}else{if(s===-1&&(e>=0?(s=0,this._setEndings(!0,this.repetitions===0,l)):this._setEndings(this.repetitions===0,!0,l)),i>=t||i<0){const c=Math.floor(i/t);i-=t*c,s+=Math.abs(c);const u=this.repetitions-s;if(u<=0)this.clampWhenFinished?this.paused=!0:this.enabled=!1,i=e>0?t:0,this.time=i,this._mixer.dispatchEvent({type:"finished",action:this,direction:e>0?1:-1});else{if(u===1){const h=e<0;this._setEndings(h,!h,l)}else this._setEndings(!1,!1,l);this._loopCount=s,this.time=i,this._mixer.dispatchEvent({type:"loop",action:this,loopDelta:c})}}else this.time=i;if(l&&(s&1)===1)return t-i}return i}_setEndings(e,t,n){const i=this._interpolantSettings;n?(i.endingStart=Ms,i.endingEnd=Ms):(e?i.endingStart=this.zeroSlopeAtStart?Ms:Ss:i.endingStart=Ba,t?i.endingEnd=this.zeroSlopeAtEnd?Ms:Ss:i.endingEnd=Ba)}_scheduleFading(e,t,n){const i=this._mixer,s=i.time;let l=this._weightInterpolant;l===null&&(l=i._lendControlInterpolant(),this._weightInterpolant=l);const c=l.parameterPositions,u=l.sampleValues;return c[0]=s,u[0]=t,c[1]=s+e,u[1]=n,this}}const _b=new Float32Array(1);class yb extends Ji{constructor(e){super(),this._root=e,this._initMemoryManager(),this._accuIndex=0,this.time=0,this.timeScale=1}_bindAction(e,t){const n=e._localRoot||this._root,i=e._clip.tracks,s=i.length,l=e._propertyBindings,c=e._interpolants,u=n.uuid,h=this._bindingsByRootAndName;let f=h[u];f===void 0&&(f={},h[u]=f);for(let p=0;p!==s;++p){const m=i[p],g=m.name;let y=f[g];if(y!==void 0)++y.referenceCount,l[p]=y;else{if(y=l[p],y!==void 0){y._cacheIndex===null&&(++y.referenceCount,this._addInactiveBinding(y,u,g));continue}const M=t&&t._propertyBindings[p].binding.parsedPath;y=new Ey(Lt.create(n,g,M),m.ValueTypeName,m.getValueSize()),++y.referenceCount,this._addInactiveBinding(y,u,g),l[p]=y}c[p].resultBuffer=y.buffer}}_activateAction(e){if(!this._isActiveAction(e)){if(e._cacheIndex===null){const n=(e._localRoot||this._root).uuid,i=e._clip.uuid,s=this._actionsByClip[i];this._bindAction(e,s&&s.knownActions[0]),this._addInactiveAction(e,i,n)}const t=e._propertyBindings;for(let n=0,i=t.length;n!==i;++n){const s=t[n];s.useCount++===0&&(this._lendBinding(s),s.saveOriginalState())}this._lendAction(e)}}_deactivateAction(e){if(this._isActiveAction(e)){const t=e._propertyBindings;for(let n=0,i=t.length;n!==i;++n){const s=t[n];--s.useCount===0&&(s.restoreOriginalState(),this._takeBackBinding(s))}this._takeBackAction(e)}}_initMemoryManager(){this._actions=[],this._nActiveActions=0,this._actionsByClip={},this._bindings=[],this._nActiveBindings=0,this._bindingsByRootAndName={},this._controlInterpolants=[],this._nActiveControlInterpolants=0;const e=this;this.stats={actions:{get total(){return e._actions.length},get inUse(){return e._nActiveActions}},bindings:{get total(){return e._bindings.length},get inUse(){return e._nActiveBindings}},controlInterpolants:{get total(){return e._controlInterpolants.length},get inUse(){return e._nActiveControlInterpolants}}}}_isActiveAction(e){const t=e._cacheIndex;return t!==null&&t<this._nActiveActions}_addInactiveAction(e,t,n){const i=this._actions,s=this._actionsByClip;let l=s[t];if(l===void 0)l={knownActions:[e],actionByRoot:{}},e._byClipCacheIndex=0,s[t]=l;else{const c=l.knownActions;e._byClipCacheIndex=c.length,c.push(e)}e._cacheIndex=i.length,i.push(e),l.actionByRoot[n]=e}_removeInactiveAction(e){const t=this._actions,n=t[t.length-1],i=e._cacheIndex;n._cacheIndex=i,t[i]=n,t.pop(),e._cacheIndex=null;const s=e._clip.uuid,l=this._actionsByClip,c=l[s],u=c.knownActions,h=u[u.length-1],f=e._byClipCacheIndex;h._byClipCacheIndex=f,u[f]=h,u.pop(),e._byClipCacheIndex=null;const p=c.actionByRoot,m=(e._localRoot||this._root).uuid;delete p[m],u.length===0&&delete l[s],this._removeInactiveBindingsForAction(e)}_removeInactiveBindingsForAction(e){const t=e._propertyBindings;for(let n=0,i=t.length;n!==i;++n){const s=t[n];--s.referenceCount===0&&this._removeInactiveBinding(s)}}_lendAction(e){const t=this._actions,n=e._cacheIndex,i=this._nActiveActions++,s=t[i];e._cacheIndex=i,t[i]=e,s._cacheIndex=n,t[n]=s}_takeBackAction(e){const t=this._actions,n=e._cacheIndex,i=--this._nActiveActions,s=t[i];e._cacheIndex=i,t[i]=e,s._cacheIndex=n,t[n]=s}_addInactiveBinding(e,t,n){const i=this._bindingsByRootAndName,s=this._bindings;let l=i[t];l===void 0&&(l={},i[t]=l),l[n]=e,e._cacheIndex=s.length,s.push(e)}_removeInactiveBinding(e){const t=this._bindings,n=e.binding,i=n.rootNode.uuid,s=n.path,l=this._bindingsByRootAndName,c=l[i],u=t[t.length-1],h=e._cacheIndex;u._cacheIndex=h,t[h]=u,t.pop(),delete c[s],Object.keys(c).length===0&&delete l[i]}_lendBinding(e){const t=this._bindings,n=e._cacheIndex,i=this._nActiveBindings++,s=t[i];e._cacheIndex=i,t[i]=e,s._cacheIndex=n,t[n]=s}_takeBackBinding(e){const t=this._bindings,n=e._cacheIndex,i=--this._nActiveBindings,s=t[i];e._cacheIndex=i,t[i]=e,s._cacheIndex=n,t[n]=s}_lendControlInterpolant(){const e=this._controlInterpolants,t=this._nActiveControlInterpolants++;let n=e[t];return n===void 0&&(n=new Np(new Float32Array(2),new Float32Array(2),1,_b),n.__cacheIndex=t,e[t]=n),n}_takeBackControlInterpolant(e){const t=this._controlInterpolants,n=e.__cacheIndex,i=--this._nActiveControlInterpolants,s=t[i];e.__cacheIndex=i,t[i]=e,s.__cacheIndex=n,t[n]=s}clipAction(e,t,n){const i=t||this._root,s=i.uuid;let l=typeof e=="string"?Za.findByName(i,e):e;const c=l!==null?l.uuid:e,u=this._actionsByClip[c];let h=null;if(n===void 0&&(l!==null?n=l.blendMode:n=sh),u!==void 0){const p=u.actionByRoot[s];if(p!==void 0&&p.blendMode===n)return p;h=u.knownActions[0],l===null&&(l=h._clip)}if(l===null)return null;const f=new wy(this,l,t,n);return this._bindAction(f,h),this._addInactiveAction(f,c,s),f}existingAction(e,t){const n=t||this._root,i=n.uuid,s=typeof e=="string"?Za.findByName(n,e):e,l=s?s.uuid:e,c=this._actionsByClip[l];return c!==void 0&&c.actionByRoot[i]||null}stopAllAction(){const e=this._actions,t=this._nActiveActions;for(let n=t-1;n>=0;--n)e[n].stop();return this}update(e){e*=this.timeScale;const t=this._actions,n=this._nActiveActions,i=this.time+=e,s=Math.sign(e),l=this._accuIndex^=1;for(let h=0;h!==n;++h)t[h]._update(i,e,s,l);const c=this._bindings,u=this._nActiveBindings;for(let h=0;h!==u;++h)c[h].apply(l);return this}setTime(e){this.time=0;for(let t=0;t<this._actions.length;t++)this._actions[t].time=0;return this.update(e)}getRoot(){return this._root}uncacheClip(e){const t=this._actions,n=e.uuid,i=this._actionsByClip,s=i[n];if(s!==void 0){const l=s.knownActions;for(let c=0,u=l.length;c!==u;++c){const h=l[c];this._deactivateAction(h);const f=h._cacheIndex,p=t[t.length-1];h._cacheIndex=null,h._byClipCacheIndex=null,p._cacheIndex=f,t[f]=p,t.pop(),this._removeInactiveBindingsForAction(h)}delete i[n]}}uncacheRoot(e){const t=e.uuid,n=this._actionsByClip;for(const l in n){const c=n[l].actionByRoot,u=c[t];u!==void 0&&(this._deactivateAction(u),this._removeInactiveAction(u))}const i=this._bindingsByRootAndName,s=i[t];if(s!==void 0)for(const l in s){const c=s[l];c.restoreOriginalState(),this._removeInactiveBinding(c)}}uncacheAction(e,t){const n=this.existingAction(e,t);n!==null&&(this._deactivateAction(n),this._removeInactiveAction(n))}}class Wp{constructor(e){this.value=e}clone(){return new Wp(this.value.clone===void 0?this.value:this.value.clone())}}let xb=0;class Sb extends Ji{constructor(){super(),this.isUniformsGroup=!0,Object.defineProperty(this,"id",{value:xb++}),this.name="",this.usage=za,this.uniforms=[]}add(e){return this.uniforms.push(e),this}remove(e){const t=this.uniforms.indexOf(e);return t!==-1&&this.uniforms.splice(t,1),this}setName(e){return this.name=e,this}setUsage(e){return this.usage=e,this}dispose(){return this.dispatchEvent({type:"dispose"}),this}copy(e){this.name=e.name,this.usage=e.usage;const t=e.uniforms;this.uniforms.length=0;for(let n=0,i=t.length;n<i;n++){const s=Array.isArray(t[n])?t[n]:[t[n]];for(let l=0;l<s.length;l++)this.uniforms.push(s[l].clone())}return this}clone(){return new this.constructor().copy(this)}}class ju extends uh{constructor(e,t,n=1){super(e,t),this.isInstancedInterleavedBuffer=!0,this.meshPerAttribute=n}copy(e){return super.copy(e),this.meshPerAttribute=e.meshPerAttribute,this}clone(e){const t=super.clone(e);return t.meshPerAttribute=this.meshPerAttribute,t}toJSON(e){const t=super.toJSON(e);return t.isInstancedInterleavedBuffer=!0,t.meshPerAttribute=this.meshPerAttribute,t}}class Mb{constructor(e,t,n,i,s){this.isGLBufferAttribute=!0,this.name="",this.buffer=e,this.type=t,this.itemSize=n,this.elementSize=i,this.count=s,this.version=0}set needsUpdate(e){e===!0&&this.version++}setBuffer(e){return this.buffer=e,this}setType(e,t){return this.type=e,this.elementSize=t,this}setItemSize(e){return this.itemSize=e,this}setCount(e){return this.count=e,this}}const K0=new ut;class Ty{constructor(e,t,n=0,i=1/0){this.ray=new Os(e,t),this.near=n,this.far=i,this.camera=null,this.layers=new Cs,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return K0.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(K0),this}intersectObject(e,t=!0,n=[]){return Kd(e,this,n,t),n.sort(Q0),n}intersectObjects(e,t=!0,n=[]){for(let i=0,s=e.length;i<s;i++)Kd(e[i],this,n,t);return n.sort(Q0),n}}function Q0(r,e){return r.distance-e.distance}function Kd(r,e,t,n){let i=!0;if(r.layers.test(e.layers)&&r.raycast(e,t)===!1&&(i=!1),i===!0&&n===!0){const s=r.children;for(let l=0,c=s.length;l<c;l++)Kd(s[l],e,t,!0)}}class Qd{constructor(e=1,t=0,n=0){return this.radius=e,this.phi=t,this.theta=n,this}set(e,t,n){return this.radius=e,this.phi=t,this.theta=n,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=Math.max(1e-6,Math.min(Math.PI-1e-6,this.phi)),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,t,n){return this.radius=Math.sqrt(e*e+t*t+n*n),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,n),this.phi=Math.acos(Jt(t/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}}class Eb{constructor(e=1,t=0,n=0){return this.radius=e,this.theta=t,this.y=n,this}set(e,t,n){return this.radius=e,this.theta=t,this.y=n,this}copy(e){return this.radius=e.radius,this.theta=e.theta,this.y=e.y,this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,t,n){return this.radius=Math.sqrt(e*e+n*n),this.theta=Math.atan2(e,n),this.y=t,this}clone(){return new this.constructor().copy(this)}}class Xp{constructor(e,t,n,i){Xp.prototype.isMatrix2=!0,this.elements=[1,0,0,1],e!==void 0&&this.set(e,t,n,i)}identity(){return this.set(1,0,0,1),this}fromArray(e,t=0){for(let n=0;n<4;n++)this.elements[n]=e[n+t];return this}set(e,t,n,i){const s=this.elements;return s[0]=e,s[2]=t,s[1]=n,s[3]=i,this}}const $0=new ae;class wb{constructor(e=new ae(1/0,1/0),t=new ae(-1/0,-1/0)){this.isBox2=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromPoints(e){this.makeEmpty();for(let t=0,n=e.length;t<n;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const n=$0.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(n),this.max.copy(e).add(n),this}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=1/0,this.max.x=this.max.y=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y}getCenter(e){return this.isEmpty()?e.set(0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,$0).distanceTo(e)}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const ev=new L,Zc=new L;class Ay{constructor(e=new L,t=new L){this.start=e,this.end=t}set(e,t){return this.start.copy(e),this.end.copy(t),this}copy(e){return this.start.copy(e.start),this.end.copy(e.end),this}getCenter(e){return e.addVectors(this.start,this.end).multiplyScalar(.5)}delta(e){return e.subVectors(this.end,this.start)}distanceSq(){return this.start.distanceToSquared(this.end)}distance(){return this.start.distanceTo(this.end)}at(e,t){return this.delta(t).multiplyScalar(e).add(this.start)}closestPointToPointParameter(e,t){ev.subVectors(e,this.start),Zc.subVectors(this.end,this.start);const n=Zc.dot(Zc);let s=Zc.dot(ev)/n;return t&&(s=Jt(s,0,1)),s}closestPointToPoint(e,t,n){const i=this.closestPointToPointParameter(e,t);return this.delta(n).multiplyScalar(i).add(this.start)}applyMatrix4(e){return this.start.applyMatrix4(e),this.end.applyMatrix4(e),this}equals(e){return e.start.equals(this.start)&&e.end.equals(this.end)}clone(){return new this.constructor().copy(this)}}const tv=new L;class Tb extends Dt{constructor(e,t){super(),this.light=e,this.matrixAutoUpdate=!1,this.color=t,this.type="SpotLightHelper";const n=new xt,i=[0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,-1,0,1,0,0,0,0,1,1,0,0,0,0,-1,1];for(let l=0,c=1,u=32;l<u;l++,c++){const h=l/u*Math.PI*2,f=c/u*Math.PI*2;i.push(Math.cos(h),Math.sin(h),1,Math.cos(f),Math.sin(f),1)}n.setAttribute("position",new Ye(i,3));const s=new Gn({fog:!1,toneMapped:!1});this.cone=new Ki(n,s),this.add(this.cone),this.update()}dispose(){this.cone.geometry.dispose(),this.cone.material.dispose()}update(){this.light.updateWorldMatrix(!0,!1),this.light.target.updateWorldMatrix(!0,!1),this.parent?(this.parent.updateWorldMatrix(!0),this.matrix.copy(this.parent.matrixWorld).invert().multiply(this.light.matrixWorld)):this.matrix.copy(this.light.matrixWorld),this.matrixWorld.copy(this.light.matrixWorld);const e=this.light.distance?this.light.distance:1e3,t=e*Math.tan(this.light.angle);this.cone.scale.set(t,t,e),tv.setFromMatrixPosition(this.light.target.matrixWorld),this.cone.lookAt(tv),this.color!==void 0?this.cone.material.color.set(this.color):this.cone.material.color.copy(this.light.color)}}const Br=new L,jc=new ut,Sd=new ut;class Ab extends Ki{constructor(e){const t=by(e),n=new xt,i=[],s=[],l=new Be(0,0,1),c=new Be(0,1,0);for(let h=0;h<t.length;h++){const f=t[h];f.parent&&f.parent.isBone&&(i.push(0,0,0),i.push(0,0,0),s.push(l.r,l.g,l.b),s.push(c.r,c.g,c.b))}n.setAttribute("position",new Ye(i,3)),n.setAttribute("color",new Ye(s,3));const u=new Gn({vertexColors:!0,depthTest:!1,depthWrite:!1,toneMapped:!1,transparent:!0});super(n,u),this.isSkeletonHelper=!0,this.type="SkeletonHelper",this.root=e,this.bones=t,this.matrix=e.matrixWorld,this.matrixAutoUpdate=!1}updateMatrixWorld(e){const t=this.bones,n=this.geometry,i=n.getAttribute("position");Sd.copy(this.root.matrixWorld).invert();for(let s=0,l=0;s<t.length;s++){const c=t[s];c.parent&&c.parent.isBone&&(jc.multiplyMatrices(Sd,c.matrixWorld),Br.setFromMatrixPosition(jc),i.setXYZ(l,Br.x,Br.y,Br.z),jc.multiplyMatrices(Sd,c.parent.matrixWorld),Br.setFromMatrixPosition(jc),i.setXYZ(l+1,Br.x,Br.y,Br.z),l+=2)}n.getAttribute("position").needsUpdate=!0,super.updateMatrixWorld(e)}dispose(){this.geometry.dispose(),this.material.dispose()}}function by(r){const e=[];r.isBone===!0&&e.push(r);for(let t=0;t<r.children.length;t++)e.push.apply(e,by(r.children[t]));return e}class bb extends nn{constructor(e,t,n){const i=new sl(t,4,2),s=new Wr({wireframe:!0,fog:!1,toneMapped:!1});super(i,s),this.light=e,this.color=n,this.type="PointLightHelper",this.matrix=this.light.matrixWorld,this.matrixAutoUpdate=!1,this.update()}dispose(){this.geometry.dispose(),this.material.dispose()}update(){this.light.updateWorldMatrix(!0,!1),this.color!==void 0?this.material.color.set(this.color):this.material.color.copy(this.light.color)}}const Cb=new L,nv=new Be,iv=new Be;class Rb extends Dt{constructor(e,t,n){super(),this.light=e,this.matrix=e.matrixWorld,this.matrixAutoUpdate=!1,this.color=n,this.type="HemisphereLightHelper";const i=new rl(t);i.rotateY(Math.PI*.5),this.material=new Wr({wireframe:!0,fog:!1,toneMapped:!1}),this.color===void 0&&(this.material.vertexColors=!0);const s=i.getAttribute("position"),l=new Float32Array(s.count*3);i.setAttribute("color",new zt(l,3)),this.add(new nn(i,this.material)),this.update()}dispose(){this.children[0].geometry.dispose(),this.children[0].material.dispose()}update(){const e=this.children[0];if(this.color!==void 0)this.material.color.set(this.color);else{const t=e.geometry.getAttribute("color");nv.copy(this.light.color),iv.copy(this.light.groundColor);for(let n=0,i=t.count;n<i;n++){const s=n<i/2?nv:iv;t.setXYZ(n,s.r,s.g,s.b)}t.needsUpdate=!0}this.light.updateWorldMatrix(!0,!1),e.lookAt(Cb.setFromMatrixPosition(this.light.matrixWorld).negate())}}class Pb extends Ki{constructor(e=10,t=10,n=4473924,i=8947848){n=new Be(n),i=new Be(i);const s=t/2,l=e/t,c=e/2,u=[],h=[];for(let m=0,g=0,y=-c;m<=t;m++,y+=l){u.push(-c,0,y,c,0,y),u.push(y,0,-c,y,0,c);const M=m===s?n:i;M.toArray(h,g),g+=3,M.toArray(h,g),g+=3,M.toArray(h,g),g+=3,M.toArray(h,g),g+=3}const f=new xt;f.setAttribute("position",new Ye(u,3)),f.setAttribute("color",new Ye(h,3));const p=new Gn({vertexColors:!0,toneMapped:!1});super(f,p),this.type="GridHelper"}dispose(){this.geometry.dispose(),this.material.dispose()}}class Ib extends Ki{constructor(e=10,t=16,n=8,i=64,s=4473924,l=8947848){s=new Be(s),l=new Be(l);const c=[],u=[];if(t>1)for(let p=0;p<t;p++){const m=p/t*(Math.PI*2),g=Math.sin(m)*e,y=Math.cos(m)*e;c.push(0,0,0),c.push(g,0,y);const M=p&1?s:l;u.push(M.r,M.g,M.b),u.push(M.r,M.g,M.b)}for(let p=0;p<n;p++){const m=p&1?s:l,g=e-e/n*p;for(let y=0;y<i;y++){let M=y/i*(Math.PI*2),x=Math.sin(M)*g,_=Math.cos(M)*g;c.push(x,0,_),u.push(m.r,m.g,m.b),M=(y+1)/i*(Math.PI*2),x=Math.sin(M)*g,_=Math.cos(M)*g,c.push(x,0,_),u.push(m.r,m.g,m.b)}}const h=new xt;h.setAttribute("position",new Ye(c,3)),h.setAttribute("color",new Ye(u,3));const f=new Gn({vertexColors:!0,toneMapped:!1});super(h,f),this.type="PolarGridHelper"}dispose(){this.geometry.dispose(),this.material.dispose()}}const rv=new L,Jc=new L,sv=new L;class Lb extends Dt{constructor(e,t,n){super(),this.light=e,this.matrix=e.matrixWorld,this.matrixAutoUpdate=!1,this.color=n,this.type="DirectionalLightHelper",t===void 0&&(t=1);let i=new xt;i.setAttribute("position",new Ye([-t,t,0,t,t,0,t,-t,0,-t,-t,0,-t,t,0],3));const s=new Gn({fog:!1,toneMapped:!1});this.lightPlane=new Vr(i,s),this.add(this.lightPlane),i=new xt,i.setAttribute("position",new Ye([0,0,0,0,0,1],3)),this.targetLine=new Vr(i,s),this.add(this.targetLine),this.update()}dispose(){this.lightPlane.geometry.dispose(),this.lightPlane.material.dispose(),this.targetLine.geometry.dispose(),this.targetLine.material.dispose()}update(){this.light.updateWorldMatrix(!0,!1),this.light.target.updateWorldMatrix(!0,!1),rv.setFromMatrixPosition(this.light.matrixWorld),Jc.setFromMatrixPosition(this.light.target.matrixWorld),sv.subVectors(Jc,rv),this.lightPlane.lookAt(Jc),this.color!==void 0?(this.lightPlane.material.color.set(this.color),this.targetLine.material.color.set(this.color)):(this.lightPlane.material.color.copy(this.light.color),this.targetLine.material.color.copy(this.light.color)),this.targetLine.lookAt(Jc),this.targetLine.scale.z=sv.length()}}const Kc=new L,jt=new el;class Db extends Ki{constructor(e){const t=new xt,n=new Gn({color:16777215,vertexColors:!0,toneMapped:!1}),i=[],s=[],l={};c("n1","n2"),c("n2","n4"),c("n4","n3"),c("n3","n1"),c("f1","f2"),c("f2","f4"),c("f4","f3"),c("f3","f1"),c("n1","f1"),c("n2","f2"),c("n3","f3"),c("n4","f4"),c("p","n1"),c("p","n2"),c("p","n3"),c("p","n4"),c("u1","u2"),c("u2","u3"),c("u3","u1"),c("c","t"),c("p","c"),c("cn1","cn2"),c("cn3","cn4"),c("cf1","cf2"),c("cf3","cf4");function c(y,M){u(y),u(M)}function u(y){i.push(0,0,0),s.push(0,0,0),l[y]===void 0&&(l[y]=[]),l[y].push(i.length/3-1)}t.setAttribute("position",new Ye(i,3)),t.setAttribute("color",new Ye(s,3)),super(t,n),this.type="CameraHelper",this.camera=e,this.camera.updateProjectionMatrix&&this.camera.updateProjectionMatrix(),this.matrix=e.matrixWorld,this.matrixAutoUpdate=!1,this.pointMap=l,this.update();const h=new Be(16755200),f=new Be(16711680),p=new Be(43775),m=new Be(16777215),g=new Be(3355443);this.setColors(h,f,p,m,g)}setColors(e,t,n,i,s){const c=this.geometry.getAttribute("color");c.setXYZ(0,e.r,e.g,e.b),c.setXYZ(1,e.r,e.g,e.b),c.setXYZ(2,e.r,e.g,e.b),c.setXYZ(3,e.r,e.g,e.b),c.setXYZ(4,e.r,e.g,e.b),c.setXYZ(5,e.r,e.g,e.b),c.setXYZ(6,e.r,e.g,e.b),c.setXYZ(7,e.r,e.g,e.b),c.setXYZ(8,e.r,e.g,e.b),c.setXYZ(9,e.r,e.g,e.b),c.setXYZ(10,e.r,e.g,e.b),c.setXYZ(11,e.r,e.g,e.b),c.setXYZ(12,e.r,e.g,e.b),c.setXYZ(13,e.r,e.g,e.b),c.setXYZ(14,e.r,e.g,e.b),c.setXYZ(15,e.r,e.g,e.b),c.setXYZ(16,e.r,e.g,e.b),c.setXYZ(17,e.r,e.g,e.b),c.setXYZ(18,e.r,e.g,e.b),c.setXYZ(19,e.r,e.g,e.b),c.setXYZ(20,e.r,e.g,e.b),c.setXYZ(21,e.r,e.g,e.b),c.setXYZ(22,e.r,e.g,e.b),c.setXYZ(23,e.r,e.g,e.b),c.setXYZ(24,t.r,t.g,t.b),c.setXYZ(25,t.r,t.g,t.b),c.setXYZ(26,t.r,t.g,t.b),c.setXYZ(27,t.r,t.g,t.b),c.setXYZ(28,t.r,t.g,t.b),c.setXYZ(29,t.r,t.g,t.b),c.setXYZ(30,t.r,t.g,t.b),c.setXYZ(31,t.r,t.g,t.b),c.setXYZ(32,n.r,n.g,n.b),c.setXYZ(33,n.r,n.g,n.b),c.setXYZ(34,n.r,n.g,n.b),c.setXYZ(35,n.r,n.g,n.b),c.setXYZ(36,n.r,n.g,n.b),c.setXYZ(37,n.r,n.g,n.b),c.setXYZ(38,i.r,i.g,i.b),c.setXYZ(39,i.r,i.g,i.b),c.setXYZ(40,s.r,s.g,s.b),c.setXYZ(41,s.r,s.g,s.b),c.setXYZ(42,s.r,s.g,s.b),c.setXYZ(43,s.r,s.g,s.b),c.setXYZ(44,s.r,s.g,s.b),c.setXYZ(45,s.r,s.g,s.b),c.setXYZ(46,s.r,s.g,s.b),c.setXYZ(47,s.r,s.g,s.b),c.setXYZ(48,s.r,s.g,s.b),c.setXYZ(49,s.r,s.g,s.b),c.needsUpdate=!0}update(){const e=this.geometry,t=this.pointMap,n=1,i=1;jt.projectionMatrixInverse.copy(this.camera.projectionMatrixInverse),en("c",t,e,jt,0,0,-1),en("t",t,e,jt,0,0,1),en("n1",t,e,jt,-n,-i,-1),en("n2",t,e,jt,n,-i,-1),en("n3",t,e,jt,-n,i,-1),en("n4",t,e,jt,n,i,-1),en("f1",t,e,jt,-n,-i,1),en("f2",t,e,jt,n,-i,1),en("f3",t,e,jt,-n,i,1),en("f4",t,e,jt,n,i,1),en("u1",t,e,jt,n*.7,i*1.1,-1),en("u2",t,e,jt,-n*.7,i*1.1,-1),en("u3",t,e,jt,0,i*2,-1),en("cf1",t,e,jt,-n,0,1),en("cf2",t,e,jt,n,0,1),en("cf3",t,e,jt,0,-i,1),en("cf4",t,e,jt,0,i,1),en("cn1",t,e,jt,-n,0,-1),en("cn2",t,e,jt,n,0,-1),en("cn3",t,e,jt,0,-i,-1),en("cn4",t,e,jt,0,i,-1),e.getAttribute("position").needsUpdate=!0}dispose(){this.geometry.dispose(),this.material.dispose()}}function en(r,e,t,n,i,s,l){Kc.set(i,s,l).unproject(n);const c=e[r];if(c!==void 0){const u=t.getAttribute("position");for(let h=0,f=c.length;h<f;h++)u.setXYZ(c[h],Kc.x,Kc.y,Kc.z)}}const Qc=new _n;class Ub extends Ki{constructor(e,t=16776960){const n=new Uint16Array([0,1,1,2,2,3,3,0,4,5,5,6,6,7,7,4,0,4,1,5,2,6,3,7]),i=new Float32Array(8*3),s=new xt;s.setIndex(new zt(n,1)),s.setAttribute("position",new zt(i,3)),super(s,new Gn({color:t,toneMapped:!1})),this.object=e,this.type="BoxHelper",this.matrixAutoUpdate=!1,this.update()}update(e){if(e!==void 0&&console.warn("THREE.BoxHelper: .update() has no longer arguments."),this.object!==void 0&&Qc.setFromObject(this.object),Qc.isEmpty())return;const t=Qc.min,n=Qc.max,i=this.geometry.attributes.position,s=i.array;s[0]=n.x,s[1]=n.y,s[2]=n.z,s[3]=t.x,s[4]=n.y,s[5]=n.z,s[6]=t.x,s[7]=t.y,s[8]=n.z,s[9]=n.x,s[10]=t.y,s[11]=n.z,s[12]=n.x,s[13]=n.y,s[14]=t.z,s[15]=t.x,s[16]=n.y,s[17]=t.z,s[18]=t.x,s[19]=t.y,s[20]=t.z,s[21]=n.x,s[22]=t.y,s[23]=t.z,i.needsUpdate=!0,this.geometry.computeBoundingSphere()}setFromObject(e){return this.object=e,this.update(),this}copy(e,t){return super.copy(e,t),this.object=e.object,this}dispose(){this.geometry.dispose(),this.material.dispose()}}class Nb extends Ki{constructor(e,t=16776960){const n=new Uint16Array([0,1,1,2,2,3,3,0,4,5,5,6,6,7,7,4,0,4,1,5,2,6,3,7]),i=[1,1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1],s=new xt;s.setIndex(new zt(n,1)),s.setAttribute("position",new Ye(i,3)),super(s,new Gn({color:t,toneMapped:!1})),this.box=e,this.type="Box3Helper",this.geometry.computeBoundingSphere()}updateMatrixWorld(e){const t=this.box;t.isEmpty()||(t.getCenter(this.position),t.getSize(this.scale),this.scale.multiplyScalar(.5),super.updateMatrixWorld(e))}dispose(){this.geometry.dispose(),this.material.dispose()}}class Ob extends Vr{constructor(e,t=1,n=16776960){const i=n,s=[1,-1,0,-1,1,0,-1,-1,0,1,1,0,-1,1,0,-1,-1,0,1,-1,0,1,1,0],l=new xt;l.setAttribute("position",new Ye(s,3)),l.computeBoundingSphere(),super(l,new Gn({color:i,toneMapped:!1})),this.type="PlaneHelper",this.plane=e,this.size=t;const c=[1,1,0,-1,1,0,-1,-1,0,1,1,0,-1,-1,0,1,-1,0],u=new xt;u.setAttribute("position",new Ye(c,3)),u.computeBoundingSphere(),this.add(new nn(u,new Wr({color:i,opacity:.2,transparent:!0,depthWrite:!1,toneMapped:!1})))}updateMatrixWorld(e){this.position.set(0,0,0),this.scale.set(.5*this.size,.5*this.size,1),this.lookAt(this.plane.normal),this.translateZ(-this.plane.constant),super.updateMatrixWorld(e)}dispose(){this.geometry.dispose(),this.material.dispose(),this.children[0].geometry.dispose(),this.children[0].material.dispose()}}const ov=new L;let $c,Md;class Fb extends Dt{constructor(e=new L(0,0,1),t=new L(0,0,0),n=1,i=16776960,s=n*.2,l=s*.2){super(),this.type="ArrowHelper",$c===void 0&&($c=new xt,$c.setAttribute("position",new Ye([0,0,0,0,1,0],3)),Md=new ko(0,.5,1,5,1),Md.translate(0,-.5,0)),this.position.copy(t),this.line=new Vr($c,new Gn({color:i,toneMapped:!1})),this.line.matrixAutoUpdate=!1,this.add(this.line),this.cone=new nn(Md,new Wr({color:i,toneMapped:!1})),this.cone.matrixAutoUpdate=!1,this.add(this.cone),this.setDirection(e),this.setLength(n,s,l)}setDirection(e){if(e.y>.99999)this.quaternion.set(0,0,0,1);else if(e.y<-.99999)this.quaternion.set(1,0,0,0);else{ov.set(e.z,0,-e.x).normalize();const t=Math.acos(e.y);this.quaternion.setFromAxisAngle(ov,t)}}setLength(e,t=e*.2,n=t*.2){this.line.scale.set(1,Math.max(1e-4,e-t),1),this.line.updateMatrix(),this.cone.scale.set(n,t,n),this.cone.position.y=e,this.cone.updateMatrix()}setColor(e){this.line.material.color.set(e),this.cone.material.color.set(e)}copy(e){return super.copy(e,!1),this.line.copy(e.line),this.cone.copy(e.cone),this}dispose(){this.line.geometry.dispose(),this.line.material.dispose(),this.cone.geometry.dispose(),this.cone.material.dispose()}}class Bb extends Ki{constructor(e=1){const t=[0,0,0,e,0,0,0,0,0,0,e,0,0,0,0,0,0,e],n=[1,0,0,1,.6,0,0,1,0,.6,1,0,0,0,1,0,.6,1],i=new xt;i.setAttribute("position",new Ye(t,3)),i.setAttribute("color",new Ye(n,3));const s=new Gn({vertexColors:!0,toneMapped:!1});super(i,s),this.type="AxesHelper"}setColors(e,t,n){const i=new Be,s=this.geometry.attributes.color.array;return i.set(e),i.toArray(s,0),i.toArray(s,3),i.set(t),i.toArray(s,6),i.toArray(s,9),i.set(n),i.toArray(s,12),i.toArray(s,15),this.geometry.attributes.color.needsUpdate=!0,this}dispose(){this.geometry.dispose(),this.material.dispose()}}class zb{constructor(){this.type="ShapePath",this.color=new Be,this.subPaths=[],this.currentPath=null}moveTo(e,t){return this.currentPath=new Va,this.subPaths.push(this.currentPath),this.currentPath.moveTo(e,t),this}lineTo(e,t){return this.currentPath.lineTo(e,t),this}quadraticCurveTo(e,t,n,i){return this.currentPath.quadraticCurveTo(e,t,n,i),this}bezierCurveTo(e,t,n,i,s,l){return this.currentPath.bezierCurveTo(e,t,n,i,s,l),this}splineThru(e){return this.currentPath.splineThru(e),this}toShapes(e){function t(_){const w=[];for(let E=0,T=_.length;E<T;E++){const U=_[E],P=new Rs;P.curves=U.curves,w.push(P)}return w}function n(_,w){const E=w.length;let T=!1;for(let U=E-1,P=0;P<E;U=P++){let D=w[U],F=w[P],C=F.x-D.x,b=F.y-D.y;if(Math.abs(b)>Number.EPSILON){if(b<0&&(D=w[P],C=-C,F=w[U],b=-b),_.y<D.y||_.y>F.y)continue;if(_.y===D.y){if(_.x===D.x)return!0}else{const N=b*(_.x-D.x)-C*(_.y-D.y);if(N===0)return!0;if(N<0)continue;T=!T}}else{if(_.y!==D.y)continue;if(F.x<=_.x&&_.x<=D.x||D.x<=_.x&&_.x<=F.x)return!0}}return T}const i=ji.isClockWise,s=this.subPaths;if(s.length===0)return[];let l,c,u;const h=[];if(s.length===1)return c=s[0],u=new Rs,u.curves=c.curves,h.push(u),h;let f=!i(s[0].getPoints());f=e?!f:f;const p=[],m=[];let g=[],y=0,M;m[y]=void 0,g[y]=[];for(let _=0,w=s.length;_<w;_++)c=s[_],M=c.getPoints(),l=i(M),l=e?!l:l,l?(!f&&m[y]&&y++,m[y]={s:new Rs,p:M},m[y].s.curves=c.curves,f&&y++,g[y]=[]):g[y].push({h:c,p:M[0]});if(!m[0])return t(s);if(m.length>1){let _=!1,w=0;for(let E=0,T=m.length;E<T;E++)p[E]=[];for(let E=0,T=m.length;E<T;E++){const U=g[E];for(let P=0;P<U.length;P++){const D=U[P];let F=!0;for(let C=0;C<m.length;C++)n(D.p,m[C].p)&&(E!==C&&w++,F?(F=!1,p[C].push(D)):_=!0);F&&p[E].push(D)}}w>0&&_===!1&&(g=p)}let x;for(let _=0,w=m.length;_<w;_++){u=m[_].s,h.push(u),x=g[_];for(let E=0,T=x.length;E<T;E++)u.holes.push(x[E].h)}return h}}class kb extends Ji{constructor(e,t=null){super(),this.object=e,this.domElement=t,this.enabled=!0,this.state=-1,this.keys={},this.mouseButtons={LEFT:null,MIDDLE:null,RIGHT:null},this.touches={ONE:null,TWO:null}}connect(){}disconnect(){}dispose(){}update(){}}class Hb extends Ci{constructor(e=1,t=1,n=1,i={}){console.warn('THREE.WebGLMultipleRenderTargets has been deprecated and will be removed in r172. Use THREE.WebGLRenderTarget and set the "count" parameter to enable MRT.'),super(e,t,{...i,count:n}),this.isWebGLMultipleRenderTargets=!0}get texture(){return this.textures}}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Ja}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Ja);const Vb=Object.freeze(Object.defineProperty({__proto__:null,ACESFilmicToneMapping:tp,AddEquation:zr,AddOperation:Kv,AdditiveAnimationBlendMode:fp,AdditiveBlending:Fd,AgXToneMapping:n_,AlphaFormat:op,AlwaysCompare:v_,AlwaysDepth:fu,AlwaysStencilFunc:Hd,AmbientLight:vy,AnimationAction:wy,AnimationClip:Za,AnimationLoader:WA,AnimationMixer:yb,AnimationObjectGroup:vb,AnimationUtils:kA,ArcCurve:G_,ArrayCamera:D_,ArrowHelper:Fb,AttachedBindMode:kd,Audio:My,AudioAnalyser:ab,AudioContext:kp,AudioListener:rb,AudioLoader:tb,AxesHelper:Bb,BackSide:Vn,BasicDepthPacking:l_,BasicShadowMap:Iv,BatchedMesh:k_,Bone:wp,BooleanKeyframeTrack:Bs,Box2:wb,Box3:_n,Box3Helper:Nb,BoxGeometry:Fs,BoxHelper:Ub,BufferAttribute:zt,BufferGeometry:xt,BufferGeometryLoader:Sy,ByteType:ip,Cache:pr,Camera:el,CameraHelper:Db,CanvasTexture:uA,CapsuleGeometry:ph,CatmullRomCurve3:W_,CineonToneMapping:e_,CircleGeometry:mh,ClampToEdgeWrapping:vi,Clock:Hp,Color:Be,ColorKeyframeTrack:Op,ColorManagement:Pt,CompressedArrayTexture:lA,CompressedCubeTexture:cA,CompressedTexture:fh,CompressedTextureLoader:XA,ConeGeometry:gh,ConstantAlphaFactor:Zv,ConstantColorFactor:Yv,Controls:kb,CubeCamera:T_,CubeReflectionMapping:_r,CubeRefractionMapping:Hr,CubeTexture:tl,CubeTextureLoader:YA,CubeUVReflectionMapping:Oo,CubicBezierCurve:bp,CubicBezierCurve3:X_,CubicInterpolant:cy,CullFaceBack:Od,CullFaceFront:Pv,CullFaceFrontBack:zx,CullFaceNone:Rv,Curve:Ri,CurvePath:q_,CustomBlending:Lv,CustomToneMapping:t_,CylinderGeometry:ko,Cylindrical:Eb,Data3DTexture:mp,DataArrayTexture:oh,DataTexture:Zi,DataTextureLoader:qA,DataUtils:QS,DecrementStencilOp:$x,DecrementWrapStencilOp:tS,DefaultLoadingManager:fy,DepthFormat:As,DepthStencilFormat:Ds,DepthTexture:yp,DetachedBindMode:r_,DirectionalLight:gy,DirectionalLightHelper:Lb,DiscreteInterpolant:uy,DodecahedronGeometry:vh,DoubleSide:Gi,DstAlphaFactor:Hv,DstColorFactor:Gv,DynamicCopyUsage:gS,DynamicDrawUsage:uS,DynamicReadUsage:dS,EdgesGeometry:Z_,EllipseCurve:dh,EqualCompare:d_,EqualDepth:pu,EqualStencilFunc:sS,EquirectangularReflectionMapping:Da,EquirectangularRefractionMapping:Ua,Euler:ai,EventDispatcher:Ji,ExtrudeGeometry:yh,FileLoader:xr,Float16BufferAttribute:rM,Float32BufferAttribute:Ye,FloatType:Kn,Fog:ch,FogExp2:lh,FramebufferTexture:aA,FrontSide:vr,Frustum:nl,GLBufferAttribute:Mb,GLSL1:_S,GLSL3:Vd,GreaterCompare:p_,GreaterDepth:gu,GreaterEqualCompare:g_,GreaterEqualDepth:mu,GreaterEqualStencilFunc:cS,GreaterStencilFunc:aS,GridHelper:Pb,Group:bo,HalfFloatType:Fo,HemisphereLight:dy,HemisphereLightHelper:Rb,IcosahedronGeometry:xh,ImageBitmapLoader:eb,ImageLoader:ja,ImageUtils:S_,IncrementStencilOp:Qx,IncrementWrapStencilOp:eS,InstancedBufferAttribute:Uo,InstancedBufferGeometry:zp,InstancedInterleavedBuffer:ju,InstancedMesh:z_,Int16BufferAttribute:nM,Int32BufferAttribute:iM,Int8BufferAttribute:$S,IntType:$u,InterleavedBuffer:uh,InterleavedBufferAttribute:si,Interpolant:ol,InterpolateDiscrete:Fa,InterpolateLinear:Wu,InterpolateSmooth:ou,InvertStencilOp:nS,KeepStencilOp:_s,KeyframeTrack:Pi,LOD:F_,LatheGeometry:il,Layers:Cs,LessCompare:f_,LessDepth:du,LessEqualCompare:dp,LessEqualDepth:Is,LessEqualStencilFunc:oS,LessStencilFunc:rS,Light:Yr,LightProbe:xy,Line:Vr,Line3:Ay,LineBasicMaterial:Gn,LineCurve:Cp,LineCurve3:Y_,LineDashedMaterial:oy,LineLoop:H_,LineSegments:Ki,LinearFilter:cn,LinearInterpolant:Np,LinearMipMapLinearFilter:Gx,LinearMipMapNearestFilter:Vx,LinearMipmapLinearFilter:Xi,LinearMipmapNearestFilter:wa,LinearSRGBColorSpace:Ns,LinearToneMapping:Qv,LinearTransfer:$a,Loader:Qn,LoaderUtils:Jd,LoadingManager:Fp,LoopOnce:s_,LoopPingPong:a_,LoopRepeat:o_,LuminanceAlphaFormat:cp,LuminanceFormat:lp,MOUSE:gs,Material:Nn,MaterialLoader:bh,MathUtils:__,Matrix2:Xp,Matrix3:gt,Matrix4:ut,MaxEquation:Ov,Mesh:nn,MeshBasicMaterial:Wr,MeshDepthMaterial:xp,MeshDistanceMaterial:Sp,MeshLambertMaterial:ry,MeshMatcapMaterial:sy,MeshNormalMaterial:iy,MeshPhongMaterial:ty,MeshPhysicalMaterial:ey,MeshStandardMaterial:Dp,MeshToonMaterial:ny,MinEquation:Nv,MirroredRepeatWrapping:Oa,MixOperation:Jv,MultiplyBlending:zd,MultiplyOperation:Ka,NearestFilter:wn,NearestMipMapLinearFilter:Hx,NearestMipMapNearestFilter:kx,NearestMipmapLinearFilter:wo,NearestMipmapNearestFilter:np,NeutralToneMapping:i_,NeverCompare:h_,NeverDepth:hu,NeverStencilFunc:iS,NoBlending:mr,NoColorSpace:fr,NoToneMapping:qi,NormalAnimationBlendMode:sh,NormalBlending:Ts,NotEqualCompare:m_,NotEqualDepth:vu,NotEqualStencilFunc:lS,NumberKeyframeTrack:Ya,Object3D:Dt,ObjectLoader:QA,ObjectSpaceNormalMap:u_,OctahedronGeometry:rl,OneFactor:Bv,OneMinusConstantAlphaFactor:jv,OneMinusConstantColorFactor:qv,OneMinusDstAlphaFactor:Vv,OneMinusDstColorFactor:Wv,OneMinusSrcAlphaFactor:uu,OneMinusSrcColorFactor:kv,OrthographicCamera:kr,PCFShadowMap:Ku,PCFSoftShadowMap:Ea,PMREMGenerator:Gd,Path:Va,PerspectiveCamera:tn,Plane:hr,PlaneGeometry:Bo,PlaneHelper:Ob,PointLight:my,PointLightHelper:bb,Points:V_,PointsMaterial:Tp,PolarGridHelper:Ib,PolyhedronGeometry:Xr,PositionalAudio:ob,PropertyBinding:Lt,PropertyMixer:Ey,QuadraticBezierCurve:Rp,QuadraticBezierCurve3:Pp,Quaternion:Un,QuaternionKeyframeTrack:al,QuaternionLinearInterpolant:hy,RED_GREEN_RGTC2_Format:Vu,RED_RGTC1_Format:hp,REVISION:Ja,RGBADepthPacking:c_,RGBAFormat:Dn,RGBAIntegerFormat:rh,RGBA_ASTC_10x10_Format:Ou,RGBA_ASTC_10x5_Format:Du,RGBA_ASTC_10x6_Format:Uu,RGBA_ASTC_10x8_Format:Nu,RGBA_ASTC_12x10_Format:Fu,RGBA_ASTC_12x12_Format:Bu,RGBA_ASTC_4x4_Format:Tu,RGBA_ASTC_5x4_Format:Au,RGBA_ASTC_5x5_Format:bu,RGBA_ASTC_6x5_Format:Cu,RGBA_ASTC_6x6_Format:Ru,RGBA_ASTC_8x5_Format:Pu,RGBA_ASTC_8x6_Format:Iu,RGBA_ASTC_8x8_Format:Lu,RGBA_BPTC_Format:Ra,RGBA_ETC2_EAC_Format:wu,RGBA_PVRTC_2BPPV1_Format:Su,RGBA_PVRTC_4BPPV1_Format:xu,RGBA_S3TC_DXT1_Format:Aa,RGBA_S3TC_DXT3_Format:ba,RGBA_S3TC_DXT5_Format:Ca,RGBDepthPacking:Zx,RGBFormat:ap,RGBIntegerFormat:Wx,RGB_BPTC_SIGNED_Format:zu,RGB_BPTC_UNSIGNED_Format:ku,RGB_ETC1_Format:Mu,RGB_ETC2_Format:Eu,RGB_PVRTC_2BPPV1_Format:yu,RGB_PVRTC_4BPPV1_Format:_u,RGB_S3TC_DXT1_Format:Ta,RGDepthPacking:jx,RGFormat:up,RGIntegerFormat:ih,RawShaderMaterial:$_,Ray:Os,Raycaster:Ty,RectAreaLight:_y,RedFormat:nh,RedIntegerFormat:Qa,ReinhardToneMapping:$v,RenderTarget:M_,RepeatWrapping:Na,ReplaceStencilOp:Kx,ReverseSubtractEquation:Uv,RingGeometry:Sh,SIGNED_RED_GREEN_RGTC2_Format:Gu,SIGNED_RED_RGTC1_Format:Hu,SRGBColorSpace:jn,SRGBTransfer:Ft,Scene:Mp,ShaderChunk:yt,ShaderLib:Ai,ShaderMaterial:_i,ShadowMaterial:Q_,Shape:Rs,ShapeGeometry:Mh,ShapePath:zb,ShapeUtils:ji,ShortType:rp,Skeleton:hh,SkeletonHelper:Ab,SkinnedMesh:B_,Source:Es,Sphere:yn,SphereGeometry:sl,Spherical:Qd,SphericalHarmonics3:yy,SplineCurve:Ip,SpotLight:py,SpotLightHelper:Tb,Sprite:O_,SpriteMaterial:Ep,SrcAlphaFactor:cu,SrcAlphaSaturateFactor:Xv,SrcColorFactor:zv,StaticCopyUsage:mS,StaticDrawUsage:za,StaticReadUsage:fS,StereoCamera:nb,StreamCopyUsage:vS,StreamDrawUsage:hS,StreamReadUsage:pS,StringKeyframeTrack:zs,SubtractEquation:Dv,SubtractiveBlending:Bd,TOUCH:vs,TangentSpaceNormalMap:Gr,TetrahedronGeometry:Eh,Texture:Kt,TextureLoader:ZA,TextureUtils:HT,TorusGeometry:wh,TorusKnotGeometry:Th,Triangle:Jn,TriangleFanDrawMode:qx,TriangleStripDrawMode:Yx,TrianglesDrawMode:Xx,TubeGeometry:Ah,UVMapping:Qu,Uint16BufferAttribute:gp,Uint32BufferAttribute:vp,Uint8BufferAttribute:eM,Uint8ClampedBufferAttribute:tM,Uniform:Wp,UniformsGroup:Sb,UniformsLib:be,UniformsUtils:Xu,UnsignedByteType:bi,UnsignedInt248Type:Ls,UnsignedInt5999Type:sp,UnsignedIntType:yr,UnsignedShort4444Type:eh,UnsignedShort5551Type:th,UnsignedShortType:Io,VSMShadowMap:wi,Vector2:ae,Vector3:L,Vector4:At,VectorKeyframeTrack:qa,VideoTexture:oA,WebGL3DRenderTarget:VS,WebGLArrayRenderTarget:HS,WebGLCoordinateSystem:Yi,WebGLCubeRenderTarget:A_,WebGLMultipleRenderTargets:Hb,WebGLRenderTarget:Ci,WebGLRenderer:U_,WebGLUtils:L_,WebGPUCoordinateSystem:ka,WireframeGeometry:Lp,WrapAroundEnding:Ba,ZeroCurvatureEnding:Ss,ZeroFactor:Fv,ZeroSlopeEnding:Ms,ZeroStencilOp:Jx,createCanvasElement:x_},Symbol.toStringTag,{value:"Module"}));var Cy={exports:{}},ks={};/**
 * @license React
 * react-reconciler-constants.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ks.ConcurrentRoot=1;ks.ContinuousEventPriority=4;ks.DefaultEventPriority=16;ks.DiscreteEventPriority=1;ks.IdleEventPriority=536870912;ks.LegacyRoot=0;Cy.exports=ks;var Ro=Cy.exports;function Gb(r){let e;const t=new Set,n=(h,f)=>{const p=typeof h=="function"?h(e):h;if(p!==e){const m=e;e=f?p:Object.assign({},e,p),t.forEach(g=>g(e,m))}},i=()=>e,s=(h,f=i,p=Object.is)=>{console.warn("[DEPRECATED] Please use `subscribeWithSelector` middleware");let m=f(e);function g(){const y=f(e);if(!p(m,y)){const M=m;h(m=y,M)}}return t.add(g),()=>t.delete(g)},u={setState:n,getState:i,subscribe:(h,f,p)=>f||p?s(h,f,p):(t.add(h),()=>t.delete(h)),destroy:()=>t.clear()};return e=r(n,i,u),u}const Wb=typeof window>"u"||!window.navigator||/ServerSideRendering|^Deno\//.test(window.navigator.userAgent),av=Wb?ke.useEffect:ke.useLayoutEffect;function Xb(r){const e=typeof r=="function"?Gb(r):r,t=(n=e.getState,i=Object.is)=>{const[,s]=ke.useReducer(x=>x+1,0),l=e.getState(),c=ke.useRef(l),u=ke.useRef(n),h=ke.useRef(i),f=ke.useRef(!1),p=ke.useRef();p.current===void 0&&(p.current=n(l));let m,g=!1;(c.current!==l||u.current!==n||h.current!==i||f.current)&&(m=n(l),g=!i(p.current,m)),av(()=>{g&&(p.current=m),c.current=l,u.current=n,h.current=i,f.current=!1});const y=ke.useRef(l);av(()=>{const x=()=>{try{const w=e.getState(),E=u.current(w);h.current(p.current,E)||(c.current=w,p.current=E,s())}catch{f.current=!0,s()}},_=e.subscribe(x);return e.getState()!==y.current&&x(),_},[]);const M=g?m:p.current;return ke.useDebugValue(M),M};return Object.assign(t,e),t[Symbol.iterator]=function(){console.warn("[useStore, api] = create() is deprecated and will be removed in v4");const n=[t,e];return{next(){const i=n.length<=0;return{value:n.shift(),done:i}}}},t}var Ry={exports:{}};/**
 * @license React
 * react-reconciler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var Yb=function(e){var t={},n=ke,i=Ud,s=Object.assign;function l(o){for(var a="https://reactjs.org/docs/error-decoder.html?invariant="+o,d=1;d<arguments.length;d++)a+="&args[]="+encodeURIComponent(arguments[d]);return"Minified React error #"+o+"; visit "+a+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var c=n.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,u=Symbol.for("react.element"),h=Symbol.for("react.portal"),f=Symbol.for("react.fragment"),p=Symbol.for("react.strict_mode"),m=Symbol.for("react.profiler"),g=Symbol.for("react.provider"),y=Symbol.for("react.context"),M=Symbol.for("react.forward_ref"),x=Symbol.for("react.suspense"),_=Symbol.for("react.suspense_list"),w=Symbol.for("react.memo"),E=Symbol.for("react.lazy"),T=Symbol.for("react.offscreen"),U=Symbol.iterator;function P(o){return o===null||typeof o!="object"?null:(o=U&&o[U]||o["@@iterator"],typeof o=="function"?o:null)}function D(o){if(o==null)return null;if(typeof o=="function")return o.displayName||o.name||null;if(typeof o=="string")return o;switch(o){case f:return"Fragment";case h:return"Portal";case m:return"Profiler";case p:return"StrictMode";case x:return"Suspense";case _:return"SuspenseList"}if(typeof o=="object")switch(o.$$typeof){case y:return(o.displayName||"Context")+".Consumer";case g:return(o._context.displayName||"Context")+".Provider";case M:var a=o.render;return o=o.displayName,o||(o=a.displayName||a.name||"",o=o!==""?"ForwardRef("+o+")":"ForwardRef"),o;case w:return a=o.displayName||null,a!==null?a:D(o.type)||"Memo";case E:a=o._payload,o=o._init;try{return D(o(a))}catch{}}return null}function F(o){var a=o.type;switch(o.tag){case 24:return"Cache";case 9:return(a.displayName||"Context")+".Consumer";case 10:return(a._context.displayName||"Context")+".Provider";case 18:return"DehydratedFragment";case 11:return o=a.render,o=o.displayName||o.name||"",a.displayName||(o!==""?"ForwardRef("+o+")":"ForwardRef");case 7:return"Fragment";case 5:return a;case 4:return"Portal";case 3:return"Root";case 6:return"Text";case 16:return D(a);case 8:return a===p?"StrictMode":"Mode";case 22:return"Offscreen";case 12:return"Profiler";case 21:return"Scope";case 13:return"Suspense";case 19:return"SuspenseList";case 25:return"TracingMarker";case 1:case 0:case 17:case 2:case 14:case 15:if(typeof a=="function")return a.displayName||a.name||null;if(typeof a=="string")return a}return null}function C(o){var a=o,d=o;if(o.alternate)for(;a.return;)a=a.return;else{o=a;do a=o,a.flags&4098&&(d=a.return),o=a.return;while(o)}return a.tag===3?d:null}function b(o){if(C(o)!==o)throw Error(l(188))}function N(o){var a=o.alternate;if(!a){if(a=C(o),a===null)throw Error(l(188));return a!==o?null:o}for(var d=o,v=a;;){var S=d.return;if(S===null)break;var A=S.alternate;if(A===null){if(v=S.return,v!==null){d=v;continue}break}if(S.child===A.child){for(A=S.child;A;){if(A===d)return b(S),o;if(A===v)return b(S),a;A=A.sibling}throw Error(l(188))}if(d.return!==v.return)d=S,v=A;else{for(var B=!1,V=S.child;V;){if(V===d){B=!0,d=S,v=A;break}if(V===v){B=!0,v=S,d=A;break}V=V.sibling}if(!B){for(V=A.child;V;){if(V===d){B=!0,d=A,v=S;break}if(V===v){B=!0,v=A,d=S;break}V=V.sibling}if(!B)throw Error(l(189))}}if(d.alternate!==v)throw Error(l(190))}if(d.tag!==3)throw Error(l(188));return d.stateNode.current===d?o:a}function q(o){return o=N(o),o!==null?Y(o):null}function Y(o){if(o.tag===5||o.tag===6)return o;for(o=o.child;o!==null;){var a=Y(o);if(a!==null)return a;o=o.sibling}return null}function K(o){if(o.tag===5||o.tag===6)return o;for(o=o.child;o!==null;){if(o.tag!==4){var a=K(o);if(a!==null)return a}o=o.sibling}return null}var le=Array.isArray,$=e.getPublicInstance,pe=e.getRootHostContext,J=e.getChildHostContext,xe=e.prepareForCommit,me=e.resetAfterCommit,Se=e.createInstance,Qe=e.appendInitialChild,Je=e.finalizeInitialChildren,se=e.prepareUpdate,ge=e.shouldSetTextContent,Ve=e.createTextInstance,we=e.scheduleTimeout,et=e.cancelTimeout,lt=e.noTimeout,tt=e.isPrimaryRenderer,ft=e.supportsMutation,he=e.supportsPersistence,de=e.supportsHydration,z=e.getInstanceFromNode,je=e.preparePortalMount,ve=e.getCurrentEventPriority,Oe=e.detachDeletedInstance,Te=e.supportsMicrotasks,it=e.scheduleMicrotask,Pe=e.supportsTestSelectors,O=e.findFiberRoot,R=e.getBoundingRect,Z=e.getTextContent,re=e.isHiddenSubtree,fe=e.matchAccessibilityRole,ce=e.setFocusIfFocusable,We=e.setupIntersectionObserver,Ae=e.appendChild,Fe=e.appendChildToContainer,St=e.commitTextUpdate,_e=e.commitMount,He=e.commitUpdate,rt=e.insertBefore,ct=e.insertInContainerBefore,ze=e.removeChild,H=e.removeChildFromContainer,oe=e.resetTextContent,Re=e.hideInstance,k=e.hideTextInstance,ye=e.unhideInstance,te=e.unhideTextInstance,ue=e.clearContainer,Ue=e.cloneInstance,Ce=e.createContainerChildSet,nt=e.appendChildToContainerChildSet,It=e.finalizeContainerChildren,Ht=e.replaceContainerChildren,bt=e.cloneHiddenInstance,rn=e.cloneHiddenTextInstance,Tn=e.canHydrateInstance,cl=e.canHydrateTextInstance,ul=e.canHydrateSuspenseInstance,Ii=e.isSuspenseInstancePending,qr=e.isSuspenseInstanceFallback,hl=e.registerSuspenseInstanceRetry,Sr=e.getNextHydratableSibling,Hs=e.getFirstHydratableChild,fl=e.getFirstHydratableChildWithinContainer,Vs=e.getFirstHydratableChildWithinSuspenseInstance,dl=e.hydrateInstance,pl=e.hydrateTextInstance,Ch=e.hydrateSuspenseInstance,Rh=e.getNextHydratableInstanceAfterSuspenseInstance,ml=e.commitHydratedContainer,I=e.commitHydratedSuspenseInstance,G=e.clearSuspenseBoundary,Q=e.clearSuspenseBoundaryFromContainer,ee=e.shouldDeleteUnhydratedTailInstances,X=e.didNotMatchHydratedContainerTextInstance,Ee=e.didNotMatchHydratedTextInstance,Ie;function Xe(o){if(Ie===void 0)try{throw Error()}catch(d){var a=d.stack.trim().match(/\n( *(at )?)/);Ie=a&&a[1]||""}return`
`+Ie+o}var qe=!1;function ht(o,a){if(!o||qe)return"";qe=!0;var d=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{if(a)if(a=function(){throw Error()},Object.defineProperty(a.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(a,[])}catch(Me){var v=Me}Reflect.construct(o,[],a)}else{try{a.call()}catch(Me){v=Me}o.call(a.prototype)}else{try{throw Error()}catch(Me){v=Me}o()}}catch(Me){if(Me&&v&&typeof Me.stack=="string"){for(var S=Me.stack.split(`
`),A=v.stack.split(`
`),B=S.length-1,V=A.length-1;1<=B&&0<=V&&S[B]!==A[V];)V--;for(;1<=B&&0<=V;B--,V--)if(S[B]!==A[V]){if(B!==1||V!==1)do if(B--,V--,0>V||S[B]!==A[V]){var ie=`
`+S[B].replace(" at new "," at ");return o.displayName&&ie.includes("<anonymous>")&&(ie=ie.replace("<anonymous>",o.displayName)),ie}while(1<=B&&0<=V);break}}}finally{qe=!1,Error.prepareStackTrace=d}return(o=o?o.displayName||o.name:"")?Xe(o):""}var dt=Object.prototype.hasOwnProperty,Ze=[],Et=-1;function Rt(o){return{current:o}}function at(o){0>Et||(o.current=Ze[Et],Ze[Et]=null,Et--)}function _t(o,a){Et++,Ze[Et]=o.current,o.current=a}var wt={},De=Rt(wt),Gt=Rt(!1),Ct=wt;function fn(o,a){var d=o.type.contextTypes;if(!d)return wt;var v=o.stateNode;if(v&&v.__reactInternalMemoizedUnmaskedChildContext===a)return v.__reactInternalMemoizedMaskedChildContext;var S={},A;for(A in d)S[A]=a[A];return v&&(o=o.stateNode,o.__reactInternalMemoizedUnmaskedChildContext=a,o.__reactInternalMemoizedMaskedChildContext=S),S}function Qt(o){return o=o.childContextTypes,o!=null}function dn(){at(Gt),at(De)}function Mr(o,a,d){if(De.current!==wt)throw Error(l(168));_t(De,a),_t(Gt,d)}function Bt(o,a,d){var v=o.stateNode;if(a=a.childContextTypes,typeof v.getChildContext!="function")return d;v=v.getChildContext();for(var S in v)if(!(S in a))throw Error(l(108,F(o)||"Unknown",S));return s({},d,v)}function On(o){return o=(o=o.stateNode)&&o.__reactInternalMemoizedMergedChildContext||wt,Ct=De.current,_t(De,o),_t(Gt,Gt.current),!0}function Er(o,a,d){var v=o.stateNode;if(!v)throw Error(l(169));d?(o=Bt(o,a,Ct),v.__reactInternalMemoizedMergedChildContext=o,at(Gt),at(De),_t(De,o)):at(Gt),_t(Gt,d)}var Wt=Math.clz32?Math.clz32:gl,Li=Math.log,Di=Math.LN2;function gl(o){return o>>>=0,o===0?32:31-(Li(o)/Di|0)|0}var vl=64,_l=4194304;function Ho(o){switch(o&-o){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return o&4194240;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return o&130023424;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 1073741824;default:return o}}function yl(o,a){var d=o.pendingLanes;if(d===0)return 0;var v=0,S=o.suspendedLanes,A=o.pingedLanes,B=d&268435455;if(B!==0){var V=B&~S;V!==0?v=Ho(V):(A&=B,A!==0&&(v=Ho(A)))}else B=d&~S,B!==0?v=Ho(B):A!==0&&(v=Ho(A));if(v===0)return 0;if(a!==0&&a!==v&&!(a&S)&&(S=v&-v,A=a&-a,S>=A||S===16&&(A&4194240)!==0))return a;if(v&4&&(v|=d&16),a=o.entangledLanes,a!==0)for(o=o.entanglements,a&=v;0<a;)d=31-Wt(a),S=1<<d,v|=o[d],a&=~S;return v}function Jy(o,a){switch(o){case 1:case 2:case 4:return a+250;case 8:case 16:case 32:case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return a+5e3;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return-1;case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Ky(o,a){for(var d=o.suspendedLanes,v=o.pingedLanes,S=o.expirationTimes,A=o.pendingLanes;0<A;){var B=31-Wt(A),V=1<<B,ie=S[B];ie===-1?(!(V&d)||V&v)&&(S[B]=Jy(V,a)):ie<=a&&(o.expiredLanes|=V),A&=~V}}function Ph(o){return o=o.pendingLanes&-1073741825,o!==0?o:o&1073741824?1073741824:0}function Ih(o){for(var a=[],d=0;31>d;d++)a.push(o);return a}function Vo(o,a,d){o.pendingLanes|=a,a!==536870912&&(o.suspendedLanes=0,o.pingedLanes=0),o=o.eventTimes,a=31-Wt(a),o[a]=d}function Qy(o,a){var d=o.pendingLanes&~a;o.pendingLanes=a,o.suspendedLanes=0,o.pingedLanes=0,o.expiredLanes&=a,o.mutableReadLanes&=a,o.entangledLanes&=a,a=o.entanglements;var v=o.eventTimes;for(o=o.expirationTimes;0<d;){var S=31-Wt(d),A=1<<S;a[S]=0,v[S]=-1,o[S]=-1,d&=~A}}function Lh(o,a){var d=o.entangledLanes|=a;for(o=o.entanglements;d;){var v=31-Wt(d),S=1<<v;S&a|o[v]&a&&(o[v]|=a),d&=~S}}var Ut=0;function Jp(o){return o&=-o,1<o?4<o?o&268435455?16:536870912:4:1}var Dh=i.unstable_scheduleCallback,Kp=i.unstable_cancelCallback,$y=i.unstable_shouldYield,ex=i.unstable_requestPaint,pn=i.unstable_now,Uh=i.unstable_ImmediatePriority,tx=i.unstable_UserBlockingPriority,Nh=i.unstable_NormalPriority,nx=i.unstable_IdlePriority,xl=null,Ui=null;function ix(o){if(Ui&&typeof Ui.onCommitFiberRoot=="function")try{Ui.onCommitFiberRoot(xl,o,void 0,(o.current.flags&128)===128)}catch{}}function rx(o,a){return o===a&&(o!==0||1/o===1/a)||o!==o&&a!==a}var Ni=typeof Object.is=="function"?Object.is:rx,Qi=null,Sl=!1,Oh=!1;function Qp(o){Qi===null?Qi=[o]:Qi.push(o)}function sx(o){Sl=!0,Qp(o)}function Oi(){if(!Oh&&Qi!==null){Oh=!0;var o=0,a=Ut;try{var d=Qi;for(Ut=1;o<d.length;o++){var v=d[o];do v=v(!0);while(v!==null)}Qi=null,Sl=!1}catch(S){throw Qi!==null&&(Qi=Qi.slice(o+1)),Dh(Uh,Oi),S}finally{Ut=a,Oh=!1}}return null}var ox=c.ReactCurrentBatchConfig;function Ml(o,a){if(Ni(o,a))return!0;if(typeof o!="object"||o===null||typeof a!="object"||a===null)return!1;var d=Object.keys(o),v=Object.keys(a);if(d.length!==v.length)return!1;for(v=0;v<d.length;v++){var S=d[v];if(!dt.call(a,S)||!Ni(o[S],a[S]))return!1}return!0}function ax(o){switch(o.tag){case 5:return Xe(o.type);case 16:return Xe("Lazy");case 13:return Xe("Suspense");case 19:return Xe("SuspenseList");case 0:case 2:case 15:return o=ht(o.type,!1),o;case 11:return o=ht(o.type.render,!1),o;case 1:return o=ht(o.type,!0),o;default:return""}}function yi(o,a){if(o&&o.defaultProps){a=s({},a),o=o.defaultProps;for(var d in o)a[d]===void 0&&(a[d]=o[d]);return a}return a}var El=Rt(null),wl=null,Gs=null,Fh=null;function Bh(){Fh=Gs=wl=null}function $p(o,a,d){tt?(_t(El,a._currentValue),a._currentValue=d):(_t(El,a._currentValue2),a._currentValue2=d)}function zh(o){var a=El.current;at(El),tt?o._currentValue=a:o._currentValue2=a}function kh(o,a,d){for(;o!==null;){var v=o.alternate;if((o.childLanes&a)!==a?(o.childLanes|=a,v!==null&&(v.childLanes|=a)):v!==null&&(v.childLanes&a)!==a&&(v.childLanes|=a),o===d)break;o=o.return}}function Ws(o,a){wl=o,Fh=Gs=null,o=o.dependencies,o!==null&&o.firstContext!==null&&(o.lanes&a&&(ti=!0),o.firstContext=null)}function li(o){var a=tt?o._currentValue:o._currentValue2;if(Fh!==o)if(o={context:o,memoizedValue:a,next:null},Gs===null){if(wl===null)throw Error(l(308));Gs=o,wl.dependencies={lanes:0,firstContext:o}}else Gs=Gs.next=o;return a}var Fi=null,wr=!1;function Hh(o){o.updateQueue={baseState:o.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,interleaved:null,lanes:0},effects:null}}function em(o,a){o=o.updateQueue,a.updateQueue===o&&(a.updateQueue={baseState:o.baseState,firstBaseUpdate:o.firstBaseUpdate,lastBaseUpdate:o.lastBaseUpdate,shared:o.shared,effects:o.effects})}function $i(o,a){return{eventTime:o,lane:a,tag:0,payload:null,callback:null,next:null}}function Tr(o,a){var d=o.updateQueue;d!==null&&(d=d.shared,sn!==null&&o.mode&1&&!(Tt&2)?(o=d.interleaved,o===null?(a.next=a,Fi===null?Fi=[d]:Fi.push(d)):(a.next=o.next,o.next=a),d.interleaved=a):(o=d.pending,o===null?a.next=a:(a.next=o.next,o.next=a),d.pending=a))}function Tl(o,a,d){if(a=a.updateQueue,a!==null&&(a=a.shared,(d&4194240)!==0)){var v=a.lanes;v&=o.pendingLanes,d|=v,a.lanes=d,Lh(o,d)}}function tm(o,a){var d=o.updateQueue,v=o.alternate;if(v!==null&&(v=v.updateQueue,d===v)){var S=null,A=null;if(d=d.firstBaseUpdate,d!==null){do{var B={eventTime:d.eventTime,lane:d.lane,tag:d.tag,payload:d.payload,callback:d.callback,next:null};A===null?S=A=B:A=A.next=B,d=d.next}while(d!==null);A===null?S=A=a:A=A.next=a}else S=A=a;d={baseState:v.baseState,firstBaseUpdate:S,lastBaseUpdate:A,shared:v.shared,effects:v.effects},o.updateQueue=d;return}o=d.lastBaseUpdate,o===null?d.firstBaseUpdate=a:o.next=a,d.lastBaseUpdate=a}function Al(o,a,d,v){var S=o.updateQueue;wr=!1;var A=S.firstBaseUpdate,B=S.lastBaseUpdate,V=S.shared.pending;if(V!==null){S.shared.pending=null;var ie=V,Me=ie.next;ie.next=null,B===null?A=Me:B.next=Me,B=ie;var Ge=o.alternate;Ge!==null&&(Ge=Ge.updateQueue,V=Ge.lastBaseUpdate,V!==B&&(V===null?Ge.firstBaseUpdate=Me:V.next=Me,Ge.lastBaseUpdate=ie))}if(A!==null){var pt=S.baseState;B=0,Ge=Me=ie=null,V=A;do{var st=V.lane,kt=V.eventTime;if((v&st)===st){Ge!==null&&(Ge=Ge.next={eventTime:kt,lane:0,tag:V.tag,payload:V.payload,callback:V.callback,next:null});e:{var $e=o,Rn=V;switch(st=a,kt=d,Rn.tag){case 1:if($e=Rn.payload,typeof $e=="function"){pt=$e.call(kt,pt,st);break e}pt=$e;break e;case 3:$e.flags=$e.flags&-65537|128;case 0:if($e=Rn.payload,st=typeof $e=="function"?$e.call(kt,pt,st):$e,st==null)break e;pt=s({},pt,st);break e;case 2:wr=!0}}V.callback!==null&&V.lane!==0&&(o.flags|=64,st=S.effects,st===null?S.effects=[V]:st.push(V))}else kt={eventTime:kt,lane:st,tag:V.tag,payload:V.payload,callback:V.callback,next:null},Ge===null?(Me=Ge=kt,ie=pt):Ge=Ge.next=kt,B|=st;if(V=V.next,V===null){if(V=S.shared.pending,V===null)break;st=V,V=st.next,st.next=null,S.lastBaseUpdate=st,S.shared.pending=null}}while(!0);if(Ge===null&&(ie=pt),S.baseState=ie,S.firstBaseUpdate=Me,S.lastBaseUpdate=Ge,a=S.shared.interleaved,a!==null){S=a;do B|=S.lane,S=S.next;while(S!==a)}else A===null&&(S.shared.lanes=0);$s|=B,o.lanes=B,o.memoizedState=pt}}function nm(o,a,d){if(o=a.effects,a.effects=null,o!==null)for(a=0;a<o.length;a++){var v=o[a],S=v.callback;if(S!==null){if(v.callback=null,v=d,typeof S!="function")throw Error(l(191,S));S.call(v)}}}var im=new n.Component().refs;function Vh(o,a,d,v){a=o.memoizedState,d=d(v,a),d=d==null?a:s({},a,d),o.memoizedState=d,o.lanes===0&&(o.updateQueue.baseState=d)}var bl={isMounted:function(o){return(o=o._reactInternals)?C(o)===o:!1},enqueueSetState:function(o,a,d){o=o._reactInternals;var v=Bn(),S=Cr(o),A=$i(v,S);A.payload=a,d!=null&&(A.callback=d),Tr(o,A),a=di(o,S,v),a!==null&&Tl(a,o,S)},enqueueReplaceState:function(o,a,d){o=o._reactInternals;var v=Bn(),S=Cr(o),A=$i(v,S);A.tag=1,A.payload=a,d!=null&&(A.callback=d),Tr(o,A),a=di(o,S,v),a!==null&&Tl(a,o,S)},enqueueForceUpdate:function(o,a){o=o._reactInternals;var d=Bn(),v=Cr(o),S=$i(d,v);S.tag=2,a!=null&&(S.callback=a),Tr(o,S),a=di(o,v,d),a!==null&&Tl(a,o,v)}};function rm(o,a,d,v,S,A,B){return o=o.stateNode,typeof o.shouldComponentUpdate=="function"?o.shouldComponentUpdate(v,A,B):a.prototype&&a.prototype.isPureReactComponent?!Ml(d,v)||!Ml(S,A):!0}function sm(o,a,d){var v=!1,S=wt,A=a.contextType;return typeof A=="object"&&A!==null?A=li(A):(S=Qt(a)?Ct:De.current,v=a.contextTypes,A=(v=v!=null)?fn(o,S):wt),a=new a(d,A),o.memoizedState=a.state!==null&&a.state!==void 0?a.state:null,a.updater=bl,o.stateNode=a,a._reactInternals=o,v&&(o=o.stateNode,o.__reactInternalMemoizedUnmaskedChildContext=S,o.__reactInternalMemoizedMaskedChildContext=A),a}function om(o,a,d,v){o=a.state,typeof a.componentWillReceiveProps=="function"&&a.componentWillReceiveProps(d,v),typeof a.UNSAFE_componentWillReceiveProps=="function"&&a.UNSAFE_componentWillReceiveProps(d,v),a.state!==o&&bl.enqueueReplaceState(a,a.state,null)}function Gh(o,a,d,v){var S=o.stateNode;S.props=d,S.state=o.memoizedState,S.refs=im,Hh(o);var A=a.contextType;typeof A=="object"&&A!==null?S.context=li(A):(A=Qt(a)?Ct:De.current,S.context=fn(o,A)),S.state=o.memoizedState,A=a.getDerivedStateFromProps,typeof A=="function"&&(Vh(o,a,A,d),S.state=o.memoizedState),typeof a.getDerivedStateFromProps=="function"||typeof S.getSnapshotBeforeUpdate=="function"||typeof S.UNSAFE_componentWillMount!="function"&&typeof S.componentWillMount!="function"||(a=S.state,typeof S.componentWillMount=="function"&&S.componentWillMount(),typeof S.UNSAFE_componentWillMount=="function"&&S.UNSAFE_componentWillMount(),a!==S.state&&bl.enqueueReplaceState(S,S.state,null),Al(o,d,S,v),S.state=o.memoizedState),typeof S.componentDidMount=="function"&&(o.flags|=4194308)}var Xs=[],Ys=0,Cl=null,Rl=0,ci=[],ui=0,Zr=null,er=1,tr="";function jr(o,a){Xs[Ys++]=Rl,Xs[Ys++]=Cl,Cl=o,Rl=a}function am(o,a,d){ci[ui++]=er,ci[ui++]=tr,ci[ui++]=Zr,Zr=o;var v=er;o=tr;var S=32-Wt(v)-1;v&=~(1<<S),d+=1;var A=32-Wt(a)+S;if(30<A){var B=S-S%5;A=(v&(1<<B)-1).toString(32),v>>=B,S-=B,er=1<<32-Wt(a)+S|d<<S|v,tr=A+o}else er=1<<A|d<<S|v,tr=o}function Wh(o){o.return!==null&&(jr(o,1),am(o,1,0))}function Xh(o){for(;o===Cl;)Cl=Xs[--Ys],Xs[Ys]=null,Rl=Xs[--Ys],Xs[Ys]=null;for(;o===Zr;)Zr=ci[--ui],ci[ui]=null,tr=ci[--ui],ci[ui]=null,er=ci[--ui],ci[ui]=null}var $n=null,ei=null,Xt=!1,Go=!1,xi=null;function lm(o,a){var d=pi(5,null,null,0);d.elementType="DELETED",d.stateNode=a,d.return=o,a=o.deletions,a===null?(o.deletions=[d],o.flags|=16):a.push(d)}function cm(o,a){switch(o.tag){case 5:return a=Tn(a,o.type,o.pendingProps),a!==null?(o.stateNode=a,$n=o,ei=Hs(a),!0):!1;case 6:return a=cl(a,o.pendingProps),a!==null?(o.stateNode=a,$n=o,ei=null,!0):!1;case 13:if(a=ul(a),a!==null){var d=Zr!==null?{id:er,overflow:tr}:null;return o.memoizedState={dehydrated:a,treeContext:d,retryLane:1073741824},d=pi(18,null,null,0),d.stateNode=a,d.return=o,o.child=d,$n=o,ei=null,!0}return!1;default:return!1}}function Yh(o){return(o.mode&1)!==0&&(o.flags&128)===0}function qh(o){if(Xt){var a=ei;if(a){var d=a;if(!cm(o,a)){if(Yh(o))throw Error(l(418));a=Sr(d);var v=$n;a&&cm(o,a)?lm(v,d):(o.flags=o.flags&-4097|2,Xt=!1,$n=o)}}else{if(Yh(o))throw Error(l(418));o.flags=o.flags&-4097|2,Xt=!1,$n=o}}}function um(o){for(o=o.return;o!==null&&o.tag!==5&&o.tag!==3&&o.tag!==13;)o=o.return;$n=o}function Wo(o){if(!de||o!==$n)return!1;if(!Xt)return um(o),Xt=!0,!1;if(o.tag!==3&&(o.tag!==5||ee(o.type)&&!ge(o.type,o.memoizedProps))){var a=ei;if(a){if(Yh(o)){for(o=ei;o;)o=Sr(o);throw Error(l(418))}for(;a;)lm(o,a),a=Sr(a)}}if(um(o),o.tag===13){if(!de)throw Error(l(316));if(o=o.memoizedState,o=o!==null?o.dehydrated:null,!o)throw Error(l(317));ei=Rh(o)}else ei=$n?Sr(o.stateNode):null;return!0}function qs(){de&&(ei=$n=null,Go=Xt=!1)}function Zh(o){xi===null?xi=[o]:xi.push(o)}function Xo(o,a,d){if(o=d.ref,o!==null&&typeof o!="function"&&typeof o!="object"){if(d._owner){if(d=d._owner,d){if(d.tag!==1)throw Error(l(309));var v=d.stateNode}if(!v)throw Error(l(147,o));var S=v,A=""+o;return a!==null&&a.ref!==null&&typeof a.ref=="function"&&a.ref._stringRef===A?a.ref:(a=function(B){var V=S.refs;V===im&&(V=S.refs={}),B===null?delete V[A]:V[A]=B},a._stringRef=A,a)}if(typeof o!="string")throw Error(l(284));if(!d._owner)throw Error(l(290,o))}return o}function Pl(o,a){throw o=Object.prototype.toString.call(a),Error(l(31,o==="[object Object]"?"object with keys {"+Object.keys(a).join(", ")+"}":o))}function hm(o){var a=o._init;return a(o._payload)}function fm(o){function a(j,W){if(o){var ne=j.deletions;ne===null?(j.deletions=[W],j.flags|=16):ne.push(W)}}function d(j,W){if(!o)return null;for(;W!==null;)a(j,W),W=W.sibling;return null}function v(j,W){for(j=new Map;W!==null;)W.key!==null?j.set(W.key,W):j.set(W.index,W),W=W.sibling;return j}function S(j,W){return j=Pr(j,W),j.index=0,j.sibling=null,j}function A(j,W,ne){return j.index=ne,o?(ne=j.alternate,ne!==null?(ne=ne.index,ne<W?(j.flags|=2,W):ne):(j.flags|=2,W)):(j.flags|=1048576,W)}function B(j){return o&&j.alternate===null&&(j.flags|=2),j}function V(j,W,ne,Ne){return W===null||W.tag!==6?(W=Lf(ne,j.mode,Ne),W.return=j,W):(W=S(W,ne),W.return=j,W)}function ie(j,W,ne,Ne){var Ke=ne.type;return Ke===f?Ge(j,W,ne.props.children,Ne,ne.key):W!==null&&(W.elementType===Ke||typeof Ke=="object"&&Ke!==null&&Ke.$$typeof===E&&hm(Ke)===W.type)?(Ne=S(W,ne.props),Ne.ref=Xo(j,W,ne),Ne.return=j,Ne):(Ne=ac(ne.type,ne.key,ne.props,null,j.mode,Ne),Ne.ref=Xo(j,W,ne),Ne.return=j,Ne)}function Me(j,W,ne,Ne){return W===null||W.tag!==4||W.stateNode.containerInfo!==ne.containerInfo||W.stateNode.implementation!==ne.implementation?(W=Df(ne,j.mode,Ne),W.return=j,W):(W=S(W,ne.children||[]),W.return=j,W)}function Ge(j,W,ne,Ne,Ke){return W===null||W.tag!==7?(W=ns(ne,j.mode,Ne,Ke),W.return=j,W):(W=S(W,ne),W.return=j,W)}function pt(j,W,ne){if(typeof W=="string"&&W!==""||typeof W=="number")return W=Lf(""+W,j.mode,ne),W.return=j,W;if(typeof W=="object"&&W!==null){switch(W.$$typeof){case u:return ne=ac(W.type,W.key,W.props,null,j.mode,ne),ne.ref=Xo(j,null,W),ne.return=j,ne;case h:return W=Df(W,j.mode,ne),W.return=j,W;case E:var Ne=W._init;return pt(j,Ne(W._payload),ne)}if(le(W)||P(W))return W=ns(W,j.mode,ne,null),W.return=j,W;Pl(j,W)}return null}function st(j,W,ne,Ne){var Ke=W!==null?W.key:null;if(typeof ne=="string"&&ne!==""||typeof ne=="number")return Ke!==null?null:V(j,W,""+ne,Ne);if(typeof ne=="object"&&ne!==null){switch(ne.$$typeof){case u:return ne.key===Ke?ie(j,W,ne,Ne):null;case h:return ne.key===Ke?Me(j,W,ne,Ne):null;case E:return Ke=ne._init,st(j,W,Ke(ne._payload),Ne)}if(le(ne)||P(ne))return Ke!==null?null:Ge(j,W,ne,Ne,null);Pl(j,ne)}return null}function kt(j,W,ne,Ne,Ke){if(typeof Ne=="string"&&Ne!==""||typeof Ne=="number")return j=j.get(ne)||null,V(W,j,""+Ne,Ke);if(typeof Ne=="object"&&Ne!==null){switch(Ne.$$typeof){case u:return j=j.get(Ne.key===null?ne:Ne.key)||null,ie(W,j,Ne,Ke);case h:return j=j.get(Ne.key===null?ne:Ne.key)||null,Me(W,j,Ne,Ke);case E:var Mt=Ne._init;return kt(j,W,ne,Mt(Ne._payload),Ke)}if(le(Ne)||P(Ne))return j=j.get(ne)||null,Ge(W,j,Ne,Ke,null);Pl(W,Ne)}return null}function $e(j,W,ne,Ne){for(var Ke=null,Mt=null,mt=W,Nt=W=0,gn=null;mt!==null&&Nt<ne.length;Nt++){mt.index>Nt?(gn=mt,mt=null):gn=mt.sibling;var Ot=st(j,mt,ne[Nt],Ne);if(Ot===null){mt===null&&(mt=gn);break}o&&mt&&Ot.alternate===null&&a(j,mt),W=A(Ot,W,Nt),Mt===null?Ke=Ot:Mt.sibling=Ot,Mt=Ot,mt=gn}if(Nt===ne.length)return d(j,mt),Xt&&jr(j,Nt),Ke;if(mt===null){for(;Nt<ne.length;Nt++)mt=pt(j,ne[Nt],Ne),mt!==null&&(W=A(mt,W,Nt),Mt===null?Ke=mt:Mt.sibling=mt,Mt=mt);return Xt&&jr(j,Nt),Ke}for(mt=v(j,mt);Nt<ne.length;Nt++)gn=kt(mt,j,Nt,ne[Nt],Ne),gn!==null&&(o&&gn.alternate!==null&&mt.delete(gn.key===null?Nt:gn.key),W=A(gn,W,Nt),Mt===null?Ke=gn:Mt.sibling=gn,Mt=gn);return o&&mt.forEach(function(Ir){return a(j,Ir)}),Xt&&jr(j,Nt),Ke}function Rn(j,W,ne,Ne){var Ke=P(ne);if(typeof Ke!="function")throw Error(l(150));if(ne=Ke.call(ne),ne==null)throw Error(l(151));for(var Mt=Ke=null,mt=W,Nt=W=0,gn=null,Ot=ne.next();mt!==null&&!Ot.done;Nt++,Ot=ne.next()){mt.index>Nt?(gn=mt,mt=null):gn=mt.sibling;var Ir=st(j,mt,Ot.value,Ne);if(Ir===null){mt===null&&(mt=gn);break}o&&mt&&Ir.alternate===null&&a(j,mt),W=A(Ir,W,Nt),Mt===null?Ke=Ir:Mt.sibling=Ir,Mt=Ir,mt=gn}if(Ot.done)return d(j,mt),Xt&&jr(j,Nt),Ke;if(mt===null){for(;!Ot.done;Nt++,Ot=ne.next())Ot=pt(j,Ot.value,Ne),Ot!==null&&(W=A(Ot,W,Nt),Mt===null?Ke=Ot:Mt.sibling=Ot,Mt=Ot);return Xt&&jr(j,Nt),Ke}for(mt=v(j,mt);!Ot.done;Nt++,Ot=ne.next())Ot=kt(mt,j,Nt,Ot.value,Ne),Ot!==null&&(o&&Ot.alternate!==null&&mt.delete(Ot.key===null?Nt:Ot.key),W=A(Ot,W,Nt),Mt===null?Ke=Ot:Mt.sibling=Ot,Mt=Ot);return o&&mt.forEach(function(Fx){return a(j,Fx)}),Xt&&jr(j,Nt),Ke}function mi(j,W,ne,Ne){if(typeof ne=="object"&&ne!==null&&ne.type===f&&ne.key===null&&(ne=ne.props.children),typeof ne=="object"&&ne!==null){switch(ne.$$typeof){case u:e:{for(var Ke=ne.key,Mt=W;Mt!==null;){if(Mt.key===Ke){if(Ke=ne.type,Ke===f){if(Mt.tag===7){d(j,Mt.sibling),W=S(Mt,ne.props.children),W.return=j,j=W;break e}}else if(Mt.elementType===Ke||typeof Ke=="object"&&Ke!==null&&Ke.$$typeof===E&&hm(Ke)===Mt.type){d(j,Mt.sibling),W=S(Mt,ne.props),W.ref=Xo(j,Mt,ne),W.return=j,j=W;break e}d(j,Mt);break}else a(j,Mt);Mt=Mt.sibling}ne.type===f?(W=ns(ne.props.children,j.mode,Ne,ne.key),W.return=j,j=W):(Ne=ac(ne.type,ne.key,ne.props,null,j.mode,Ne),Ne.ref=Xo(j,W,ne),Ne.return=j,j=Ne)}return B(j);case h:e:{for(Mt=ne.key;W!==null;){if(W.key===Mt)if(W.tag===4&&W.stateNode.containerInfo===ne.containerInfo&&W.stateNode.implementation===ne.implementation){d(j,W.sibling),W=S(W,ne.children||[]),W.return=j,j=W;break e}else{d(j,W);break}else a(j,W);W=W.sibling}W=Df(ne,j.mode,Ne),W.return=j,j=W}return B(j);case E:return Mt=ne._init,mi(j,W,Mt(ne._payload),Ne)}if(le(ne))return $e(j,W,ne,Ne);if(P(ne))return Rn(j,W,ne,Ne);Pl(j,ne)}return typeof ne=="string"&&ne!==""||typeof ne=="number"?(ne=""+ne,W!==null&&W.tag===6?(d(j,W.sibling),W=S(W,ne),W.return=j,j=W):(d(j,W),W=Lf(ne,j.mode,Ne),W.return=j,j=W),B(j)):d(j,W)}return mi}var Zs=fm(!0),dm=fm(!1),Yo={},hi=Rt(Yo),qo=Rt(Yo),js=Rt(Yo);function Bi(o){if(o===Yo)throw Error(l(174));return o}function jh(o,a){_t(js,a),_t(qo,o),_t(hi,Yo),o=pe(a),at(hi),_t(hi,o)}function Js(){at(hi),at(qo),at(js)}function pm(o){var a=Bi(js.current),d=Bi(hi.current);a=J(d,o.type,a),d!==a&&(_t(qo,o),_t(hi,a))}function Jh(o){qo.current===o&&(at(hi),at(qo))}var Yt=Rt(0);function Il(o){for(var a=o;a!==null;){if(a.tag===13){var d=a.memoizedState;if(d!==null&&(d=d.dehydrated,d===null||Ii(d)||qr(d)))return a}else if(a.tag===19&&a.memoizedProps.revealOrder!==void 0){if(a.flags&128)return a}else if(a.child!==null){a.child.return=a,a=a.child;continue}if(a===o)break;for(;a.sibling===null;){if(a.return===null||a.return===o)return null;a=a.return}a.sibling.return=a.return,a=a.sibling}return null}var Kh=[];function Qh(){for(var o=0;o<Kh.length;o++){var a=Kh[o];tt?a._workInProgressVersionPrimary=null:a._workInProgressVersionSecondary=null}Kh.length=0}var Ll=c.ReactCurrentDispatcher,fi=c.ReactCurrentBatchConfig,Ks=0,Zt=null,An=null,mn=null,Dl=!1,Zo=!1,jo=0,lx=0;function bn(){throw Error(l(321))}function $h(o,a){if(a===null)return!1;for(var d=0;d<a.length&&d<o.length;d++)if(!Ni(o[d],a[d]))return!1;return!0}function ef(o,a,d,v,S,A){if(Ks=A,Zt=a,a.memoizedState=null,a.updateQueue=null,a.lanes=0,Ll.current=o===null||o.memoizedState===null?fx:dx,o=d(v,S),Zo){A=0;do{if(Zo=!1,jo=0,25<=A)throw Error(l(301));A+=1,mn=An=null,a.updateQueue=null,Ll.current=px,o=d(v,S)}while(Zo)}if(Ll.current=Bl,a=An!==null&&An.next!==null,Ks=0,mn=An=Zt=null,Dl=!1,a)throw Error(l(300));return o}function tf(){var o=jo!==0;return jo=0,o}function nr(){var o={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return mn===null?Zt.memoizedState=mn=o:mn=mn.next=o,mn}function zi(){if(An===null){var o=Zt.alternate;o=o!==null?o.memoizedState:null}else o=An.next;var a=mn===null?Zt.memoizedState:mn.next;if(a!==null)mn=a,An=o;else{if(o===null)throw Error(l(310));An=o,o={memoizedState:An.memoizedState,baseState:An.baseState,baseQueue:An.baseQueue,queue:An.queue,next:null},mn===null?Zt.memoizedState=mn=o:mn=mn.next=o}return mn}function Jr(o,a){return typeof a=="function"?a(o):a}function Ul(o){var a=zi(),d=a.queue;if(d===null)throw Error(l(311));d.lastRenderedReducer=o;var v=An,S=v.baseQueue,A=d.pending;if(A!==null){if(S!==null){var B=S.next;S.next=A.next,A.next=B}v.baseQueue=S=A,d.pending=null}if(S!==null){A=S.next,v=v.baseState;var V=B=null,ie=null,Me=A;do{var Ge=Me.lane;if((Ks&Ge)===Ge)ie!==null&&(ie=ie.next={lane:0,action:Me.action,hasEagerState:Me.hasEagerState,eagerState:Me.eagerState,next:null}),v=Me.hasEagerState?Me.eagerState:o(v,Me.action);else{var pt={lane:Ge,action:Me.action,hasEagerState:Me.hasEagerState,eagerState:Me.eagerState,next:null};ie===null?(V=ie=pt,B=v):ie=ie.next=pt,Zt.lanes|=Ge,$s|=Ge}Me=Me.next}while(Me!==null&&Me!==A);ie===null?B=v:ie.next=V,Ni(v,a.memoizedState)||(ti=!0),a.memoizedState=v,a.baseState=B,a.baseQueue=ie,d.lastRenderedState=v}if(o=d.interleaved,o!==null){S=o;do A=S.lane,Zt.lanes|=A,$s|=A,S=S.next;while(S!==o)}else S===null&&(d.lanes=0);return[a.memoizedState,d.dispatch]}function Nl(o){var a=zi(),d=a.queue;if(d===null)throw Error(l(311));d.lastRenderedReducer=o;var v=d.dispatch,S=d.pending,A=a.memoizedState;if(S!==null){d.pending=null;var B=S=S.next;do A=o(A,B.action),B=B.next;while(B!==S);Ni(A,a.memoizedState)||(ti=!0),a.memoizedState=A,a.baseQueue===null&&(a.baseState=A),d.lastRenderedState=A}return[A,v]}function mm(){}function gm(o,a){var d=Zt,v=zi(),S=a(),A=!Ni(v.memoizedState,S);if(A&&(v.memoizedState=S,ti=!0),v=v.queue,Ko(ym.bind(null,d,v,o),[o]),v.getSnapshot!==a||A||mn!==null&&mn.memoizedState.tag&1){if(d.flags|=2048,Jo(9,_m.bind(null,d,v,S,a),void 0,null),sn===null)throw Error(l(349));Ks&30||vm(d,a,S)}return S}function vm(o,a,d){o.flags|=16384,o={getSnapshot:a,value:d},a=Zt.updateQueue,a===null?(a={lastEffect:null,stores:null},Zt.updateQueue=a,a.stores=[o]):(d=a.stores,d===null?a.stores=[o]:d.push(o))}function _m(o,a,d,v){a.value=d,a.getSnapshot=v,xm(a)&&di(o,1,-1)}function ym(o,a,d){return d(function(){xm(a)&&di(o,1,-1)})}function xm(o){var a=o.getSnapshot;o=o.value;try{var d=a();return!Ni(o,d)}catch{return!0}}function nf(o){var a=nr();return typeof o=="function"&&(o=o()),a.memoizedState=a.baseState=o,o={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:Jr,lastRenderedState:o},a.queue=o,o=o.dispatch=hx.bind(null,Zt,o),[a.memoizedState,o]}function Jo(o,a,d,v){return o={tag:o,create:a,destroy:d,deps:v,next:null},a=Zt.updateQueue,a===null?(a={lastEffect:null,stores:null},Zt.updateQueue=a,a.lastEffect=o.next=o):(d=a.lastEffect,d===null?a.lastEffect=o.next=o:(v=d.next,d.next=o,o.next=v,a.lastEffect=o)),o}function Sm(){return zi().memoizedState}function Ol(o,a,d,v){var S=nr();Zt.flags|=o,S.memoizedState=Jo(1|a,d,void 0,v===void 0?null:v)}function Fl(o,a,d,v){var S=zi();v=v===void 0?null:v;var A=void 0;if(An!==null){var B=An.memoizedState;if(A=B.destroy,v!==null&&$h(v,B.deps)){S.memoizedState=Jo(a,d,A,v);return}}Zt.flags|=o,S.memoizedState=Jo(1|a,d,A,v)}function rf(o,a){return Ol(8390656,8,o,a)}function Ko(o,a){return Fl(2048,8,o,a)}function Mm(o,a){return Fl(4,2,o,a)}function Em(o,a){return Fl(4,4,o,a)}function wm(o,a){if(typeof a=="function")return o=o(),a(o),function(){a(null)};if(a!=null)return o=o(),a.current=o,function(){a.current=null}}function Tm(o,a,d){return d=d!=null?d.concat([o]):null,Fl(4,4,wm.bind(null,a,o),d)}function sf(){}function Am(o,a){var d=zi();a=a===void 0?null:a;var v=d.memoizedState;return v!==null&&a!==null&&$h(a,v[1])?v[0]:(d.memoizedState=[o,a],o)}function bm(o,a){var d=zi();a=a===void 0?null:a;var v=d.memoizedState;return v!==null&&a!==null&&$h(a,v[1])?v[0]:(o=o(),d.memoizedState=[o,a],o)}function cx(o,a){var d=Ut;Ut=d!==0&&4>d?d:4,o(!0);var v=fi.transition;fi.transition={};try{o(!1),a()}finally{Ut=d,fi.transition=v}}function Cm(){return zi().memoizedState}function ux(o,a,d){var v=Cr(o);d={lane:v,action:d,hasEagerState:!1,eagerState:null,next:null},Rm(o)?Pm(a,d):(Im(o,a,d),d=Bn(),o=di(o,v,d),o!==null&&Lm(o,a,v))}function hx(o,a,d){var v=Cr(o),S={lane:v,action:d,hasEagerState:!1,eagerState:null,next:null};if(Rm(o))Pm(a,S);else{Im(o,a,S);var A=o.alternate;if(o.lanes===0&&(A===null||A.lanes===0)&&(A=a.lastRenderedReducer,A!==null))try{var B=a.lastRenderedState,V=A(B,d);if(S.hasEagerState=!0,S.eagerState=V,Ni(V,B))return}catch{}finally{}d=Bn(),o=di(o,v,d),o!==null&&Lm(o,a,v)}}function Rm(o){var a=o.alternate;return o===Zt||a!==null&&a===Zt}function Pm(o,a){Zo=Dl=!0;var d=o.pending;d===null?a.next=a:(a.next=d.next,d.next=a),o.pending=a}function Im(o,a,d){sn!==null&&o.mode&1&&!(Tt&2)?(o=a.interleaved,o===null?(d.next=d,Fi===null?Fi=[a]:Fi.push(a)):(d.next=o.next,o.next=d),a.interleaved=d):(o=a.pending,o===null?d.next=d:(d.next=o.next,o.next=d),a.pending=d)}function Lm(o,a,d){if(d&4194240){var v=a.lanes;v&=o.pendingLanes,d|=v,a.lanes=d,Lh(o,d)}}var Bl={readContext:li,useCallback:bn,useContext:bn,useEffect:bn,useImperativeHandle:bn,useInsertionEffect:bn,useLayoutEffect:bn,useMemo:bn,useReducer:bn,useRef:bn,useState:bn,useDebugValue:bn,useDeferredValue:bn,useTransition:bn,useMutableSource:bn,useSyncExternalStore:bn,useId:bn,unstable_isNewReconciler:!1},fx={readContext:li,useCallback:function(o,a){return nr().memoizedState=[o,a===void 0?null:a],o},useContext:li,useEffect:rf,useImperativeHandle:function(o,a,d){return d=d!=null?d.concat([o]):null,Ol(4194308,4,wm.bind(null,a,o),d)},useLayoutEffect:function(o,a){return Ol(4194308,4,o,a)},useInsertionEffect:function(o,a){return Ol(4,2,o,a)},useMemo:function(o,a){var d=nr();return a=a===void 0?null:a,o=o(),d.memoizedState=[o,a],o},useReducer:function(o,a,d){var v=nr();return a=d!==void 0?d(a):a,v.memoizedState=v.baseState=a,o={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:o,lastRenderedState:a},v.queue=o,o=o.dispatch=ux.bind(null,Zt,o),[v.memoizedState,o]},useRef:function(o){var a=nr();return o={current:o},a.memoizedState=o},useState:nf,useDebugValue:sf,useDeferredValue:function(o){var a=nf(o),d=a[0],v=a[1];return rf(function(){var S=fi.transition;fi.transition={};try{v(o)}finally{fi.transition=S}},[o]),d},useTransition:function(){var o=nf(!1),a=o[0];return o=cx.bind(null,o[1]),nr().memoizedState=o,[a,o]},useMutableSource:function(){},useSyncExternalStore:function(o,a,d){var v=Zt,S=nr();if(Xt){if(d===void 0)throw Error(l(407));d=d()}else{if(d=a(),sn===null)throw Error(l(349));Ks&30||vm(v,a,d)}S.memoizedState=d;var A={value:d,getSnapshot:a};return S.queue=A,rf(ym.bind(null,v,A,o),[o]),v.flags|=2048,Jo(9,_m.bind(null,v,A,d,a),void 0,null),d},useId:function(){var o=nr(),a=sn.identifierPrefix;if(Xt){var d=tr,v=er;d=(v&~(1<<32-Wt(v)-1)).toString(32)+d,a=":"+a+"R"+d,d=jo++,0<d&&(a+="H"+d.toString(32)),a+=":"}else d=lx++,a=":"+a+"r"+d.toString(32)+":";return o.memoizedState=a},unstable_isNewReconciler:!1},dx={readContext:li,useCallback:Am,useContext:li,useEffect:Ko,useImperativeHandle:Tm,useInsertionEffect:Mm,useLayoutEffect:Em,useMemo:bm,useReducer:Ul,useRef:Sm,useState:function(){return Ul(Jr)},useDebugValue:sf,useDeferredValue:function(o){var a=Ul(Jr),d=a[0],v=a[1];return Ko(function(){var S=fi.transition;fi.transition={};try{v(o)}finally{fi.transition=S}},[o]),d},useTransition:function(){var o=Ul(Jr)[0],a=zi().memoizedState;return[o,a]},useMutableSource:mm,useSyncExternalStore:gm,useId:Cm,unstable_isNewReconciler:!1},px={readContext:li,useCallback:Am,useContext:li,useEffect:Ko,useImperativeHandle:Tm,useInsertionEffect:Mm,useLayoutEffect:Em,useMemo:bm,useReducer:Nl,useRef:Sm,useState:function(){return Nl(Jr)},useDebugValue:sf,useDeferredValue:function(o){var a=Nl(Jr),d=a[0],v=a[1];return Ko(function(){var S=fi.transition;fi.transition={};try{v(o)}finally{fi.transition=S}},[o]),d},useTransition:function(){var o=Nl(Jr)[0],a=zi().memoizedState;return[o,a]},useMutableSource:mm,useSyncExternalStore:gm,useId:Cm,unstable_isNewReconciler:!1};function of(o,a){try{var d="",v=a;do d+=ax(v),v=v.return;while(v);var S=d}catch(A){S=`
Error generating stack: `+A.message+`
`+A.stack}return{value:o,source:a,stack:S}}function af(o,a){try{console.error(a.value)}catch(d){setTimeout(function(){throw d})}}var mx=typeof WeakMap=="function"?WeakMap:Map;function Dm(o,a,d){d=$i(-1,d),d.tag=3,d.payload={element:null};var v=a.value;return d.callback=function(){ec||(ec=!0,Tf=v),af(o,a)},d}function Um(o,a,d){d=$i(-1,d),d.tag=3;var v=o.type.getDerivedStateFromError;if(typeof v=="function"){var S=a.value;d.payload=function(){return v(S)},d.callback=function(){af(o,a)}}var A=o.stateNode;return A!==null&&typeof A.componentDidCatch=="function"&&(d.callback=function(){af(o,a),typeof v!="function"&&(Ar===null?Ar=new Set([this]):Ar.add(this));var B=a.stack;this.componentDidCatch(a.value,{componentStack:B!==null?B:""})}),d}function Nm(o,a,d){var v=o.pingCache;if(v===null){v=o.pingCache=new mx;var S=new Set;v.set(a,S)}else S=v.get(a),S===void 0&&(S=new Set,v.set(a,S));S.has(d)||(S.add(d),o=Rx.bind(null,o,a,d),a.then(o,o))}function Om(o){do{var a;if((a=o.tag===13)&&(a=o.memoizedState,a=a!==null?a.dehydrated!==null:!0),a)return o;o=o.return}while(o!==null);return null}function Fm(o,a,d,v,S){return o.mode&1?(o.flags|=65536,o.lanes=S,o):(o===a?o.flags|=65536:(o.flags|=128,d.flags|=131072,d.flags&=-52805,d.tag===1&&(d.alternate===null?d.tag=17:(a=$i(-1,1),a.tag=2,Tr(d,a))),d.lanes|=1),o)}function ki(o){o.flags|=4}function Bm(o,a){if(o!==null&&o.child===a.child)return!0;if(a.flags&16)return!1;for(o=a.child;o!==null;){if(o.flags&12854||o.subtreeFlags&12854)return!1;o=o.sibling}return!0}var Qo,$o,zl,kl;if(ft)Qo=function(o,a){for(var d=a.child;d!==null;){if(d.tag===5||d.tag===6)Qe(o,d.stateNode);else if(d.tag!==4&&d.child!==null){d.child.return=d,d=d.child;continue}if(d===a)break;for(;d.sibling===null;){if(d.return===null||d.return===a)return;d=d.return}d.sibling.return=d.return,d=d.sibling}},$o=function(){},zl=function(o,a,d,v,S){if(o=o.memoizedProps,o!==v){var A=a.stateNode,B=Bi(hi.current);d=se(A,d,o,v,S,B),(a.updateQueue=d)&&ki(a)}},kl=function(o,a,d,v){d!==v&&ki(a)};else if(he){Qo=function(o,a,d,v){for(var S=a.child;S!==null;){if(S.tag===5){var A=S.stateNode;d&&v&&(A=bt(A,S.type,S.memoizedProps,S)),Qe(o,A)}else if(S.tag===6)A=S.stateNode,d&&v&&(A=rn(A,S.memoizedProps,S)),Qe(o,A);else if(S.tag!==4){if(S.tag===22&&S.memoizedState!==null)A=S.child,A!==null&&(A.return=S),Qo(o,S,!0,!0);else if(S.child!==null){S.child.return=S,S=S.child;continue}}if(S===a)break;for(;S.sibling===null;){if(S.return===null||S.return===a)return;S=S.return}S.sibling.return=S.return,S=S.sibling}};var zm=function(o,a,d,v){for(var S=a.child;S!==null;){if(S.tag===5){var A=S.stateNode;d&&v&&(A=bt(A,S.type,S.memoizedProps,S)),nt(o,A)}else if(S.tag===6)A=S.stateNode,d&&v&&(A=rn(A,S.memoizedProps,S)),nt(o,A);else if(S.tag!==4){if(S.tag===22&&S.memoizedState!==null)A=S.child,A!==null&&(A.return=S),zm(o,S,!0,!0);else if(S.child!==null){S.child.return=S,S=S.child;continue}}if(S===a)break;for(;S.sibling===null;){if(S.return===null||S.return===a)return;S=S.return}S.sibling.return=S.return,S=S.sibling}};$o=function(o,a){var d=a.stateNode;if(!Bm(o,a)){o=d.containerInfo;var v=Ce(o);zm(v,a,!1,!1),d.pendingChildren=v,ki(a),It(o,v)}},zl=function(o,a,d,v,S){var A=o.stateNode,B=o.memoizedProps;if((o=Bm(o,a))&&B===v)a.stateNode=A;else{var V=a.stateNode,ie=Bi(hi.current),Me=null;B!==v&&(Me=se(V,d,B,v,S,ie)),o&&Me===null?a.stateNode=A:(A=Ue(A,Me,d,B,v,a,o,V),Je(A,d,v,S,ie)&&ki(a),a.stateNode=A,o?ki(a):Qo(A,a,!1,!1))}},kl=function(o,a,d,v){d!==v?(o=Bi(js.current),d=Bi(hi.current),a.stateNode=Ve(v,o,d,a),ki(a)):a.stateNode=o.stateNode}}else $o=function(){},zl=function(){},kl=function(){};function ea(o,a){if(!Xt)switch(o.tailMode){case"hidden":a=o.tail;for(var d=null;a!==null;)a.alternate!==null&&(d=a),a=a.sibling;d===null?o.tail=null:d.sibling=null;break;case"collapsed":d=o.tail;for(var v=null;d!==null;)d.alternate!==null&&(v=d),d=d.sibling;v===null?a||o.tail===null?o.tail=null:o.tail.sibling=null:v.sibling=null}}function Cn(o){var a=o.alternate!==null&&o.alternate.child===o.child,d=0,v=0;if(a)for(var S=o.child;S!==null;)d|=S.lanes|S.childLanes,v|=S.subtreeFlags&14680064,v|=S.flags&14680064,S.return=o,S=S.sibling;else for(S=o.child;S!==null;)d|=S.lanes|S.childLanes,v|=S.subtreeFlags,v|=S.flags,S.return=o,S=S.sibling;return o.subtreeFlags|=v,o.childLanes=d,a}function gx(o,a,d){var v=a.pendingProps;switch(Xh(a),a.tag){case 2:case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return Cn(a),null;case 1:return Qt(a.type)&&dn(),Cn(a),null;case 3:return v=a.stateNode,Js(),at(Gt),at(De),Qh(),v.pendingContext&&(v.context=v.pendingContext,v.pendingContext=null),(o===null||o.child===null)&&(Wo(a)?ki(a):o===null||o.memoizedState.isDehydrated&&!(a.flags&256)||(a.flags|=1024,xi!==null&&(Cf(xi),xi=null))),$o(o,a),Cn(a),null;case 5:Jh(a),d=Bi(js.current);var S=a.type;if(o!==null&&a.stateNode!=null)zl(o,a,S,v,d),o.ref!==a.ref&&(a.flags|=512,a.flags|=2097152);else{if(!v){if(a.stateNode===null)throw Error(l(166));return Cn(a),null}if(o=Bi(hi.current),Wo(a)){if(!de)throw Error(l(175));o=dl(a.stateNode,a.type,a.memoizedProps,d,o,a,!Go),a.updateQueue=o,o!==null&&ki(a)}else{var A=Se(S,v,d,o,a);Qo(A,a,!1,!1),a.stateNode=A,Je(A,S,v,d,o)&&ki(a)}a.ref!==null&&(a.flags|=512,a.flags|=2097152)}return Cn(a),null;case 6:if(o&&a.stateNode!=null)kl(o,a,o.memoizedProps,v);else{if(typeof v!="string"&&a.stateNode===null)throw Error(l(166));if(o=Bi(js.current),d=Bi(hi.current),Wo(a)){if(!de)throw Error(l(176));if(o=a.stateNode,v=a.memoizedProps,(d=pl(o,v,a,!Go))&&(S=$n,S!==null))switch(A=(S.mode&1)!==0,S.tag){case 3:X(S.stateNode.containerInfo,o,v,A);break;case 5:Ee(S.type,S.memoizedProps,S.stateNode,o,v,A)}d&&ki(a)}else a.stateNode=Ve(v,o,d,a)}return Cn(a),null;case 13:if(at(Yt),v=a.memoizedState,Xt&&ei!==null&&a.mode&1&&!(a.flags&128)){for(o=ei;o;)o=Sr(o);return qs(),a.flags|=98560,a}if(v!==null&&v.dehydrated!==null){if(v=Wo(a),o===null){if(!v)throw Error(l(318));if(!de)throw Error(l(344));if(o=a.memoizedState,o=o!==null?o.dehydrated:null,!o)throw Error(l(317));Ch(o,a)}else qs(),!(a.flags&128)&&(a.memoizedState=null),a.flags|=4;return Cn(a),null}return xi!==null&&(Cf(xi),xi=null),a.flags&128?(a.lanes=d,a):(v=v!==null,d=!1,o===null?Wo(a):d=o.memoizedState!==null,v&&!d&&(a.child.flags|=8192,a.mode&1&&(o===null||Yt.current&1?ln===0&&(ln=3):Pf())),a.updateQueue!==null&&(a.flags|=4),Cn(a),null);case 4:return Js(),$o(o,a),o===null&&je(a.stateNode.containerInfo),Cn(a),null;case 10:return zh(a.type._context),Cn(a),null;case 17:return Qt(a.type)&&dn(),Cn(a),null;case 19:if(at(Yt),S=a.memoizedState,S===null)return Cn(a),null;if(v=(a.flags&128)!==0,A=S.rendering,A===null)if(v)ea(S,!1);else{if(ln!==0||o!==null&&o.flags&128)for(o=a.child;o!==null;){if(A=Il(o),A!==null){for(a.flags|=128,ea(S,!1),o=A.updateQueue,o!==null&&(a.updateQueue=o,a.flags|=4),a.subtreeFlags=0,o=d,v=a.child;v!==null;)d=v,S=o,d.flags&=14680066,A=d.alternate,A===null?(d.childLanes=0,d.lanes=S,d.child=null,d.subtreeFlags=0,d.memoizedProps=null,d.memoizedState=null,d.updateQueue=null,d.dependencies=null,d.stateNode=null):(d.childLanes=A.childLanes,d.lanes=A.lanes,d.child=A.child,d.subtreeFlags=0,d.deletions=null,d.memoizedProps=A.memoizedProps,d.memoizedState=A.memoizedState,d.updateQueue=A.updateQueue,d.type=A.type,S=A.dependencies,d.dependencies=S===null?null:{lanes:S.lanes,firstContext:S.firstContext}),v=v.sibling;return _t(Yt,Yt.current&1|2),a.child}o=o.sibling}S.tail!==null&&pn()>wf&&(a.flags|=128,v=!0,ea(S,!1),a.lanes=4194304)}else{if(!v)if(o=Il(A),o!==null){if(a.flags|=128,v=!0,o=o.updateQueue,o!==null&&(a.updateQueue=o,a.flags|=4),ea(S,!0),S.tail===null&&S.tailMode==="hidden"&&!A.alternate&&!Xt)return Cn(a),null}else 2*pn()-S.renderingStartTime>wf&&d!==1073741824&&(a.flags|=128,v=!0,ea(S,!1),a.lanes=4194304);S.isBackwards?(A.sibling=a.child,a.child=A):(o=S.last,o!==null?o.sibling=A:a.child=A,S.last=A)}return S.tail!==null?(a=S.tail,S.rendering=a,S.tail=a.sibling,S.renderingStartTime=pn(),a.sibling=null,o=Yt.current,_t(Yt,v?o&1|2:o&1),a):(Cn(a),null);case 22:case 23:return Rf(),v=a.memoizedState!==null,o!==null&&o.memoizedState!==null!==v&&(a.flags|=8192),v&&a.mode&1?ni&1073741824&&(Cn(a),ft&&a.subtreeFlags&6&&(a.flags|=8192)):Cn(a),null;case 24:return null;case 25:return null}throw Error(l(156,a.tag))}var vx=c.ReactCurrentOwner,ti=!1;function Fn(o,a,d,v){a.child=o===null?dm(a,null,d,v):Zs(a,o.child,d,v)}function km(o,a,d,v,S){d=d.render;var A=a.ref;return Ws(a,S),v=ef(o,a,d,v,A,S),d=tf(),o!==null&&!ti?(a.updateQueue=o.updateQueue,a.flags&=-2053,o.lanes&=~S,ir(o,a,S)):(Xt&&d&&Wh(a),a.flags|=1,Fn(o,a,v,S),a.child)}function Hm(o,a,d,v,S){if(o===null){var A=d.type;return typeof A=="function"&&!If(A)&&A.defaultProps===void 0&&d.compare===null&&d.defaultProps===void 0?(a.tag=15,a.type=A,Vm(o,a,A,v,S)):(o=ac(d.type,null,v,a,a.mode,S),o.ref=a.ref,o.return=a,a.child=o)}if(A=o.child,!(o.lanes&S)){var B=A.memoizedProps;if(d=d.compare,d=d!==null?d:Ml,d(B,v)&&o.ref===a.ref)return ir(o,a,S)}return a.flags|=1,o=Pr(A,v),o.ref=a.ref,o.return=a,a.child=o}function Vm(o,a,d,v,S){if(o!==null&&Ml(o.memoizedProps,v)&&o.ref===a.ref)if(ti=!1,(o.lanes&S)!==0)o.flags&131072&&(ti=!0);else return a.lanes=o.lanes,ir(o,a,S);return lf(o,a,d,v,S)}function Gm(o,a,d){var v=a.pendingProps,S=v.children,A=o!==null?o.memoizedState:null;if(v.mode==="hidden")if(!(a.mode&1))a.memoizedState={baseLanes:0,cachePool:null},_t(Qs,ni),ni|=d;else if(d&1073741824)a.memoizedState={baseLanes:0,cachePool:null},v=A!==null?A.baseLanes:d,_t(Qs,ni),ni|=v;else return o=A!==null?A.baseLanes|d:d,a.lanes=a.childLanes=1073741824,a.memoizedState={baseLanes:o,cachePool:null},a.updateQueue=null,_t(Qs,ni),ni|=o,null;else A!==null?(v=A.baseLanes|d,a.memoizedState=null):v=d,_t(Qs,ni),ni|=v;return Fn(o,a,S,d),a.child}function Wm(o,a){var d=a.ref;(o===null&&d!==null||o!==null&&o.ref!==d)&&(a.flags|=512,a.flags|=2097152)}function lf(o,a,d,v,S){var A=Qt(d)?Ct:De.current;return A=fn(a,A),Ws(a,S),d=ef(o,a,d,v,A,S),v=tf(),o!==null&&!ti?(a.updateQueue=o.updateQueue,a.flags&=-2053,o.lanes&=~S,ir(o,a,S)):(Xt&&v&&Wh(a),a.flags|=1,Fn(o,a,d,S),a.child)}function Xm(o,a,d,v,S){if(Qt(d)){var A=!0;On(a)}else A=!1;if(Ws(a,S),a.stateNode===null)o!==null&&(o.alternate=null,a.alternate=null,a.flags|=2),sm(a,d,v),Gh(a,d,v,S),v=!0;else if(o===null){var B=a.stateNode,V=a.memoizedProps;B.props=V;var ie=B.context,Me=d.contextType;typeof Me=="object"&&Me!==null?Me=li(Me):(Me=Qt(d)?Ct:De.current,Me=fn(a,Me));var Ge=d.getDerivedStateFromProps,pt=typeof Ge=="function"||typeof B.getSnapshotBeforeUpdate=="function";pt||typeof B.UNSAFE_componentWillReceiveProps!="function"&&typeof B.componentWillReceiveProps!="function"||(V!==v||ie!==Me)&&om(a,B,v,Me),wr=!1;var st=a.memoizedState;B.state=st,Al(a,v,B,S),ie=a.memoizedState,V!==v||st!==ie||Gt.current||wr?(typeof Ge=="function"&&(Vh(a,d,Ge,v),ie=a.memoizedState),(V=wr||rm(a,d,V,v,st,ie,Me))?(pt||typeof B.UNSAFE_componentWillMount!="function"&&typeof B.componentWillMount!="function"||(typeof B.componentWillMount=="function"&&B.componentWillMount(),typeof B.UNSAFE_componentWillMount=="function"&&B.UNSAFE_componentWillMount()),typeof B.componentDidMount=="function"&&(a.flags|=4194308)):(typeof B.componentDidMount=="function"&&(a.flags|=4194308),a.memoizedProps=v,a.memoizedState=ie),B.props=v,B.state=ie,B.context=Me,v=V):(typeof B.componentDidMount=="function"&&(a.flags|=4194308),v=!1)}else{B=a.stateNode,em(o,a),V=a.memoizedProps,Me=a.type===a.elementType?V:yi(a.type,V),B.props=Me,pt=a.pendingProps,st=B.context,ie=d.contextType,typeof ie=="object"&&ie!==null?ie=li(ie):(ie=Qt(d)?Ct:De.current,ie=fn(a,ie));var kt=d.getDerivedStateFromProps;(Ge=typeof kt=="function"||typeof B.getSnapshotBeforeUpdate=="function")||typeof B.UNSAFE_componentWillReceiveProps!="function"&&typeof B.componentWillReceiveProps!="function"||(V!==pt||st!==ie)&&om(a,B,v,ie),wr=!1,st=a.memoizedState,B.state=st,Al(a,v,B,S);var $e=a.memoizedState;V!==pt||st!==$e||Gt.current||wr?(typeof kt=="function"&&(Vh(a,d,kt,v),$e=a.memoizedState),(Me=wr||rm(a,d,Me,v,st,$e,ie)||!1)?(Ge||typeof B.UNSAFE_componentWillUpdate!="function"&&typeof B.componentWillUpdate!="function"||(typeof B.componentWillUpdate=="function"&&B.componentWillUpdate(v,$e,ie),typeof B.UNSAFE_componentWillUpdate=="function"&&B.UNSAFE_componentWillUpdate(v,$e,ie)),typeof B.componentDidUpdate=="function"&&(a.flags|=4),typeof B.getSnapshotBeforeUpdate=="function"&&(a.flags|=1024)):(typeof B.componentDidUpdate!="function"||V===o.memoizedProps&&st===o.memoizedState||(a.flags|=4),typeof B.getSnapshotBeforeUpdate!="function"||V===o.memoizedProps&&st===o.memoizedState||(a.flags|=1024),a.memoizedProps=v,a.memoizedState=$e),B.props=v,B.state=$e,B.context=ie,v=Me):(typeof B.componentDidUpdate!="function"||V===o.memoizedProps&&st===o.memoizedState||(a.flags|=4),typeof B.getSnapshotBeforeUpdate!="function"||V===o.memoizedProps&&st===o.memoizedState||(a.flags|=1024),v=!1)}return cf(o,a,d,v,A,S)}function cf(o,a,d,v,S,A){Wm(o,a);var B=(a.flags&128)!==0;if(!v&&!B)return S&&Er(a,d,!1),ir(o,a,A);v=a.stateNode,vx.current=a;var V=B&&typeof d.getDerivedStateFromError!="function"?null:v.render();return a.flags|=1,o!==null&&B?(a.child=Zs(a,o.child,null,A),a.child=Zs(a,null,V,A)):Fn(o,a,V,A),a.memoizedState=v.state,S&&Er(a,d,!0),a.child}function Ym(o){var a=o.stateNode;a.pendingContext?Mr(o,a.pendingContext,a.pendingContext!==a.context):a.context&&Mr(o,a.context,!1),jh(o,a.containerInfo)}function qm(o,a,d,v,S){return qs(),Zh(S),a.flags|=256,Fn(o,a,d,v),a.child}var Hl={dehydrated:null,treeContext:null,retryLane:0};function Vl(o){return{baseLanes:o,cachePool:null}}function Zm(o,a,d){var v=a.pendingProps,S=Yt.current,A=!1,B=(a.flags&128)!==0,V;if((V=B)||(V=o!==null&&o.memoizedState===null?!1:(S&2)!==0),V?(A=!0,a.flags&=-129):(o===null||o.memoizedState!==null)&&(S|=1),_t(Yt,S&1),o===null)return qh(a),o=a.memoizedState,o!==null&&(o=o.dehydrated,o!==null)?(a.mode&1?qr(o)?a.lanes=8:a.lanes=1073741824:a.lanes=1,null):(S=v.children,o=v.fallback,A?(v=a.mode,A=a.child,S={mode:"hidden",children:S},!(v&1)&&A!==null?(A.childLanes=0,A.pendingProps=S):A=lc(S,v,0,null),o=ns(o,v,d,null),A.return=a,o.return=a,A.sibling=o,a.child=A,a.child.memoizedState=Vl(d),a.memoizedState=Hl,o):uf(a,S));if(S=o.memoizedState,S!==null){if(V=S.dehydrated,V!==null){if(B)return a.flags&256?(a.flags&=-257,Gl(o,a,d,Error(l(422)))):a.memoizedState!==null?(a.child=o.child,a.flags|=128,null):(A=v.fallback,S=a.mode,v=lc({mode:"visible",children:v.children},S,0,null),A=ns(A,S,d,null),A.flags|=2,v.return=a,A.return=a,v.sibling=A,a.child=v,a.mode&1&&Zs(a,o.child,null,d),a.child.memoizedState=Vl(d),a.memoizedState=Hl,A);if(!(a.mode&1))a=Gl(o,a,d,null);else if(qr(V))a=Gl(o,a,d,Error(l(419)));else if(v=(d&o.childLanes)!==0,ti||v){if(v=sn,v!==null){switch(d&-d){case 4:A=2;break;case 16:A=8;break;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:A=32;break;case 536870912:A=268435456;break;default:A=0}v=A&(v.suspendedLanes|d)?0:A,v!==0&&v!==S.retryLane&&(S.retryLane=v,di(o,v,-1))}Pf(),a=Gl(o,a,d,Error(l(421)))}else Ii(V)?(a.flags|=128,a.child=o.child,a=Px.bind(null,o),hl(V,a),a=null):(d=S.treeContext,de&&(ei=Vs(V),$n=a,Xt=!0,xi=null,Go=!1,d!==null&&(ci[ui++]=er,ci[ui++]=tr,ci[ui++]=Zr,er=d.id,tr=d.overflow,Zr=a)),a=uf(a,a.pendingProps.children),a.flags|=4096);return a}return A?(v=Jm(o,a,v.children,v.fallback,d),A=a.child,S=o.child.memoizedState,A.memoizedState=S===null?Vl(d):{baseLanes:S.baseLanes|d,cachePool:null},A.childLanes=o.childLanes&~d,a.memoizedState=Hl,v):(d=jm(o,a,v.children,d),a.memoizedState=null,d)}return A?(v=Jm(o,a,v.children,v.fallback,d),A=a.child,S=o.child.memoizedState,A.memoizedState=S===null?Vl(d):{baseLanes:S.baseLanes|d,cachePool:null},A.childLanes=o.childLanes&~d,a.memoizedState=Hl,v):(d=jm(o,a,v.children,d),a.memoizedState=null,d)}function uf(o,a){return a=lc({mode:"visible",children:a},o.mode,0,null),a.return=o,o.child=a}function jm(o,a,d,v){var S=o.child;return o=S.sibling,d=Pr(S,{mode:"visible",children:d}),!(a.mode&1)&&(d.lanes=v),d.return=a,d.sibling=null,o!==null&&(v=a.deletions,v===null?(a.deletions=[o],a.flags|=16):v.push(o)),a.child=d}function Jm(o,a,d,v,S){var A=a.mode;o=o.child;var B=o.sibling,V={mode:"hidden",children:d};return!(A&1)&&a.child!==o?(d=a.child,d.childLanes=0,d.pendingProps=V,a.deletions=null):(d=Pr(o,V),d.subtreeFlags=o.subtreeFlags&14680064),B!==null?v=Pr(B,v):(v=ns(v,A,S,null),v.flags|=2),v.return=a,d.return=a,d.sibling=v,a.child=d,v}function Gl(o,a,d,v){return v!==null&&Zh(v),Zs(a,o.child,null,d),o=uf(a,a.pendingProps.children),o.flags|=2,a.memoizedState=null,o}function Km(o,a,d){o.lanes|=a;var v=o.alternate;v!==null&&(v.lanes|=a),kh(o.return,a,d)}function hf(o,a,d,v,S){var A=o.memoizedState;A===null?o.memoizedState={isBackwards:a,rendering:null,renderingStartTime:0,last:v,tail:d,tailMode:S}:(A.isBackwards=a,A.rendering=null,A.renderingStartTime=0,A.last=v,A.tail=d,A.tailMode=S)}function Qm(o,a,d){var v=a.pendingProps,S=v.revealOrder,A=v.tail;if(Fn(o,a,v.children,d),v=Yt.current,v&2)v=v&1|2,a.flags|=128;else{if(o!==null&&o.flags&128)e:for(o=a.child;o!==null;){if(o.tag===13)o.memoizedState!==null&&Km(o,d,a);else if(o.tag===19)Km(o,d,a);else if(o.child!==null){o.child.return=o,o=o.child;continue}if(o===a)break e;for(;o.sibling===null;){if(o.return===null||o.return===a)break e;o=o.return}o.sibling.return=o.return,o=o.sibling}v&=1}if(_t(Yt,v),!(a.mode&1))a.memoizedState=null;else switch(S){case"forwards":for(d=a.child,S=null;d!==null;)o=d.alternate,o!==null&&Il(o)===null&&(S=d),d=d.sibling;d=S,d===null?(S=a.child,a.child=null):(S=d.sibling,d.sibling=null),hf(a,!1,S,d,A);break;case"backwards":for(d=null,S=a.child,a.child=null;S!==null;){if(o=S.alternate,o!==null&&Il(o)===null){a.child=S;break}o=S.sibling,S.sibling=d,d=S,S=o}hf(a,!0,d,null,A);break;case"together":hf(a,!1,null,null,void 0);break;default:a.memoizedState=null}return a.child}function ir(o,a,d){if(o!==null&&(a.dependencies=o.dependencies),$s|=a.lanes,!(d&a.childLanes))return null;if(o!==null&&a.child!==o.child)throw Error(l(153));if(a.child!==null){for(o=a.child,d=Pr(o,o.pendingProps),a.child=d,d.return=a;o.sibling!==null;)o=o.sibling,d=d.sibling=Pr(o,o.pendingProps),d.return=a;d.sibling=null}return a.child}function _x(o,a,d){switch(a.tag){case 3:Ym(a),qs();break;case 5:pm(a);break;case 1:Qt(a.type)&&On(a);break;case 4:jh(a,a.stateNode.containerInfo);break;case 10:$p(a,a.type._context,a.memoizedProps.value);break;case 13:var v=a.memoizedState;if(v!==null)return v.dehydrated!==null?(_t(Yt,Yt.current&1),a.flags|=128,null):d&a.child.childLanes?Zm(o,a,d):(_t(Yt,Yt.current&1),o=ir(o,a,d),o!==null?o.sibling:null);_t(Yt,Yt.current&1);break;case 19:if(v=(d&a.childLanes)!==0,o.flags&128){if(v)return Qm(o,a,d);a.flags|=128}var S=a.memoizedState;if(S!==null&&(S.rendering=null,S.tail=null,S.lastEffect=null),_t(Yt,Yt.current),v)break;return null;case 22:case 23:return a.lanes=0,Gm(o,a,d)}return ir(o,a,d)}function yx(o,a){switch(Xh(a),a.tag){case 1:return Qt(a.type)&&dn(),o=a.flags,o&65536?(a.flags=o&-65537|128,a):null;case 3:return Js(),at(Gt),at(De),Qh(),o=a.flags,o&65536&&!(o&128)?(a.flags=o&-65537|128,a):null;case 5:return Jh(a),null;case 13:if(at(Yt),o=a.memoizedState,o!==null&&o.dehydrated!==null){if(a.alternate===null)throw Error(l(340));qs()}return o=a.flags,o&65536?(a.flags=o&-65537|128,a):null;case 19:return at(Yt),null;case 4:return Js(),null;case 10:return zh(a.type._context),null;case 22:case 23:return Rf(),null;case 24:return null;default:return null}}var Wl=!1,Kr=!1,xx=typeof WeakSet=="function"?WeakSet:Set,Le=null;function Xl(o,a){var d=o.ref;if(d!==null)if(typeof d=="function")try{d(null)}catch(v){Yn(o,a,v)}else d.current=null}function ff(o,a,d){try{d()}catch(v){Yn(o,a,v)}}var $m=!1;function Sx(o,a){for(xe(o.containerInfo),Le=a;Le!==null;)if(o=Le,a=o.child,(o.subtreeFlags&1028)!==0&&a!==null)a.return=o,Le=a;else for(;Le!==null;){o=Le;try{var d=o.alternate;if(o.flags&1024)switch(o.tag){case 0:case 11:case 15:break;case 1:if(d!==null){var v=d.memoizedProps,S=d.memoizedState,A=o.stateNode,B=A.getSnapshotBeforeUpdate(o.elementType===o.type?v:yi(o.type,v),S);A.__reactInternalSnapshotBeforeUpdate=B}break;case 3:ft&&ue(o.stateNode.containerInfo);break;case 5:case 6:case 4:case 17:break;default:throw Error(l(163))}}catch(V){Yn(o,o.return,V)}if(a=o.sibling,a!==null){a.return=o.return,Le=a;break}Le=o.return}return d=$m,$m=!1,d}function Qr(o,a,d){var v=a.updateQueue;if(v=v!==null?v.lastEffect:null,v!==null){var S=v=v.next;do{if((S.tag&o)===o){var A=S.destroy;S.destroy=void 0,A!==void 0&&ff(a,d,A)}S=S.next}while(S!==v)}}function ta(o,a){if(a=a.updateQueue,a=a!==null?a.lastEffect:null,a!==null){var d=a=a.next;do{if((d.tag&o)===o){var v=d.create;d.destroy=v()}d=d.next}while(d!==a)}}function df(o){var a=o.ref;if(a!==null){var d=o.stateNode;switch(o.tag){case 5:o=$(d);break;default:o=d}typeof a=="function"?a(o):a.current=o}}function eg(o,a,d){if(Ui&&typeof Ui.onCommitFiberUnmount=="function")try{Ui.onCommitFiberUnmount(xl,a)}catch{}switch(a.tag){case 0:case 11:case 14:case 15:if(o=a.updateQueue,o!==null&&(o=o.lastEffect,o!==null)){var v=o=o.next;do{var S=v,A=S.destroy;S=S.tag,A!==void 0&&(S&2||S&4)&&ff(a,d,A),v=v.next}while(v!==o)}break;case 1:if(Xl(a,d),o=a.stateNode,typeof o.componentWillUnmount=="function")try{o.props=a.memoizedProps,o.state=a.memoizedState,o.componentWillUnmount()}catch(B){Yn(a,d,B)}break;case 5:Xl(a,d);break;case 4:ft?og(o,a,d):he&&he&&(a=a.stateNode.containerInfo,d=Ce(a),Ht(a,d))}}function tg(o,a,d){for(var v=a;;)if(eg(o,v,d),v.child===null||ft&&v.tag===4){if(v===a)break;for(;v.sibling===null;){if(v.return===null||v.return===a)return;v=v.return}v.sibling.return=v.return,v=v.sibling}else v.child.return=v,v=v.child}function ng(o){var a=o.alternate;a!==null&&(o.alternate=null,ng(a)),o.child=null,o.deletions=null,o.sibling=null,o.tag===5&&(a=o.stateNode,a!==null&&Oe(a)),o.stateNode=null,o.return=null,o.dependencies=null,o.memoizedProps=null,o.memoizedState=null,o.pendingProps=null,o.stateNode=null,o.updateQueue=null}function ig(o){return o.tag===5||o.tag===3||o.tag===4}function rg(o){e:for(;;){for(;o.sibling===null;){if(o.return===null||ig(o.return))return null;o=o.return}for(o.sibling.return=o.return,o=o.sibling;o.tag!==5&&o.tag!==6&&o.tag!==18;){if(o.flags&2||o.child===null||o.tag===4)continue e;o.child.return=o,o=o.child}if(!(o.flags&2))return o.stateNode}}function sg(o){if(ft){e:{for(var a=o.return;a!==null;){if(ig(a))break e;a=a.return}throw Error(l(160))}var d=a;switch(d.tag){case 5:a=d.stateNode,d.flags&32&&(oe(a),d.flags&=-33),d=rg(o),mf(o,d,a);break;case 3:case 4:a=d.stateNode.containerInfo,d=rg(o),pf(o,d,a);break;default:throw Error(l(161))}}}function pf(o,a,d){var v=o.tag;if(v===5||v===6)o=o.stateNode,a?ct(d,o,a):Fe(d,o);else if(v!==4&&(o=o.child,o!==null))for(pf(o,a,d),o=o.sibling;o!==null;)pf(o,a,d),o=o.sibling}function mf(o,a,d){var v=o.tag;if(v===5||v===6)o=o.stateNode,a?rt(d,o,a):Ae(d,o);else if(v!==4&&(o=o.child,o!==null))for(mf(o,a,d),o=o.sibling;o!==null;)mf(o,a,d),o=o.sibling}function og(o,a,d){for(var v=a,S=!1,A,B;;){if(!S){S=v.return;e:for(;;){if(S===null)throw Error(l(160));switch(A=S.stateNode,S.tag){case 5:B=!1;break e;case 3:A=A.containerInfo,B=!0;break e;case 4:A=A.containerInfo,B=!0;break e}S=S.return}S=!0}if(v.tag===5||v.tag===6)tg(o,v,d),B?H(A,v.stateNode):ze(A,v.stateNode);else if(v.tag===18)B?Q(A,v.stateNode):G(A,v.stateNode);else if(v.tag===4){if(v.child!==null){A=v.stateNode.containerInfo,B=!0,v.child.return=v,v=v.child;continue}}else if(eg(o,v,d),v.child!==null){v.child.return=v,v=v.child;continue}if(v===a)break;for(;v.sibling===null;){if(v.return===null||v.return===a)return;v=v.return,v.tag===4&&(S=!1)}v.sibling.return=v.return,v=v.sibling}}function gf(o,a){if(ft){switch(a.tag){case 0:case 11:case 14:case 15:Qr(3,a,a.return),ta(3,a),Qr(5,a,a.return);return;case 1:return;case 5:var d=a.stateNode;if(d!=null){var v=a.memoizedProps;o=o!==null?o.memoizedProps:v;var S=a.type,A=a.updateQueue;a.updateQueue=null,A!==null&&He(d,A,S,o,v,a)}return;case 6:if(a.stateNode===null)throw Error(l(162));d=a.memoizedProps,St(a.stateNode,o!==null?o.memoizedProps:d,d);return;case 3:de&&o!==null&&o.memoizedState.isDehydrated&&ml(a.stateNode.containerInfo);return;case 12:return;case 13:Yl(a);return;case 19:Yl(a);return;case 17:return}throw Error(l(163))}switch(a.tag){case 0:case 11:case 14:case 15:Qr(3,a,a.return),ta(3,a),Qr(5,a,a.return);return;case 12:return;case 13:Yl(a);return;case 19:Yl(a);return;case 3:de&&o!==null&&o.memoizedState.isDehydrated&&ml(a.stateNode.containerInfo);break;case 22:case 23:return}e:if(he){switch(a.tag){case 1:case 5:case 6:break e;case 3:case 4:a=a.stateNode,Ht(a.containerInfo,a.pendingChildren);break e}throw Error(l(163))}}function Yl(o){var a=o.updateQueue;if(a!==null){o.updateQueue=null;var d=o.stateNode;d===null&&(d=o.stateNode=new xx),a.forEach(function(v){var S=Ix.bind(null,o,v);d.has(v)||(d.add(v),v.then(S,S))})}}function Mx(o,a){for(Le=a;Le!==null;){a=Le;var d=a.deletions;if(d!==null)for(var v=0;v<d.length;v++){var S=d[v];try{var A=o;ft?og(A,S,a):tg(A,S,a);var B=S.alternate;B!==null&&(B.return=null),S.return=null}catch(Ke){Yn(S,a,Ke)}}if(d=a.child,a.subtreeFlags&12854&&d!==null)d.return=a,Le=d;else for(;Le!==null;){a=Le;try{var V=a.flags;if(V&32&&ft&&oe(a.stateNode),V&512){var ie=a.alternate;if(ie!==null){var Me=ie.ref;Me!==null&&(typeof Me=="function"?Me(null):Me.current=null)}}if(V&8192)switch(a.tag){case 13:if(a.memoizedState!==null){var Ge=a.alternate;(Ge===null||Ge.memoizedState===null)&&(Ef=pn())}break;case 22:var pt=a.memoizedState!==null,st=a.alternate,kt=st!==null&&st.memoizedState!==null;if(d=a,ft){e:if(v=d,S=pt,A=null,ft)for(var $e=v;;){if($e.tag===5){if(A===null){A=$e;var Rn=$e.stateNode;S?Re(Rn):ye($e.stateNode,$e.memoizedProps)}}else if($e.tag===6){if(A===null){var mi=$e.stateNode;S?k(mi):te(mi,$e.memoizedProps)}}else if(($e.tag!==22&&$e.tag!==23||$e.memoizedState===null||$e===v)&&$e.child!==null){$e.child.return=$e,$e=$e.child;continue}if($e===v)break;for(;$e.sibling===null;){if($e.return===null||$e.return===v)break e;A===$e&&(A=null),$e=$e.return}A===$e&&(A=null),$e.sibling.return=$e.return,$e=$e.sibling}}if(pt&&!kt&&d.mode&1){Le=d;for(var j=d.child;j!==null;){for(d=Le=j;Le!==null;){v=Le;var W=v.child;switch(v.tag){case 0:case 11:case 14:case 15:Qr(4,v,v.return);break;case 1:Xl(v,v.return);var ne=v.stateNode;if(typeof ne.componentWillUnmount=="function"){var Ne=v.return;try{ne.props=v.memoizedProps,ne.state=v.memoizedState,ne.componentWillUnmount()}catch(Ke){Yn(v,Ne,Ke)}}break;case 5:Xl(v,v.return);break;case 22:if(v.memoizedState!==null){cg(d);continue}}W!==null?(W.return=v,Le=W):cg(d)}j=j.sibling}}}switch(V&4102){case 2:sg(a),a.flags&=-3;break;case 6:sg(a),a.flags&=-3,gf(a.alternate,a);break;case 4096:a.flags&=-4097;break;case 4100:a.flags&=-4097,gf(a.alternate,a);break;case 4:gf(a.alternate,a)}}catch(Ke){Yn(a,a.return,Ke)}if(d=a.sibling,d!==null){d.return=a.return,Le=d;break}Le=a.return}}}function Ex(o,a,d){Le=o,ag(o)}function ag(o,a,d){for(var v=(o.mode&1)!==0;Le!==null;){var S=Le,A=S.child;if(S.tag===22&&v){var B=S.memoizedState!==null||Wl;if(!B){var V=S.alternate,ie=V!==null&&V.memoizedState!==null||Kr;V=Wl;var Me=Kr;if(Wl=B,(Kr=ie)&&!Me)for(Le=S;Le!==null;)B=Le,ie=B.child,B.tag===22&&B.memoizedState!==null?ug(S):ie!==null?(ie.return=B,Le=ie):ug(S);for(;A!==null;)Le=A,ag(A),A=A.sibling;Le=S,Wl=V,Kr=Me}lg(o)}else S.subtreeFlags&8772&&A!==null?(A.return=S,Le=A):lg(o)}}function lg(o){for(;Le!==null;){var a=Le;if(a.flags&8772){var d=a.alternate;try{if(a.flags&8772)switch(a.tag){case 0:case 11:case 15:Kr||ta(5,a);break;case 1:var v=a.stateNode;if(a.flags&4&&!Kr)if(d===null)v.componentDidMount();else{var S=a.elementType===a.type?d.memoizedProps:yi(a.type,d.memoizedProps);v.componentDidUpdate(S,d.memoizedState,v.__reactInternalSnapshotBeforeUpdate)}var A=a.updateQueue;A!==null&&nm(a,A,v);break;case 3:var B=a.updateQueue;if(B!==null){if(d=null,a.child!==null)switch(a.child.tag){case 5:d=$(a.child.stateNode);break;case 1:d=a.child.stateNode}nm(a,B,d)}break;case 5:var V=a.stateNode;d===null&&a.flags&4&&_e(V,a.type,a.memoizedProps,a);break;case 6:break;case 4:break;case 12:break;case 13:if(de&&a.memoizedState===null){var ie=a.alternate;if(ie!==null){var Me=ie.memoizedState;if(Me!==null){var Ge=Me.dehydrated;Ge!==null&&I(Ge)}}}break;case 19:case 17:case 21:case 22:case 23:break;default:throw Error(l(163))}Kr||a.flags&512&&df(a)}catch(pt){Yn(a,a.return,pt)}}if(a===o){Le=null;break}if(d=a.sibling,d!==null){d.return=a.return,Le=d;break}Le=a.return}}function cg(o){for(;Le!==null;){var a=Le;if(a===o){Le=null;break}var d=a.sibling;if(d!==null){d.return=a.return,Le=d;break}Le=a.return}}function ug(o){for(;Le!==null;){var a=Le;try{switch(a.tag){case 0:case 11:case 15:var d=a.return;try{ta(4,a)}catch(ie){Yn(a,d,ie)}break;case 1:var v=a.stateNode;if(typeof v.componentDidMount=="function"){var S=a.return;try{v.componentDidMount()}catch(ie){Yn(a,S,ie)}}var A=a.return;try{df(a)}catch(ie){Yn(a,A,ie)}break;case 5:var B=a.return;try{df(a)}catch(ie){Yn(a,B,ie)}}}catch(ie){Yn(a,a.return,ie)}if(a===o){Le=null;break}var V=a.sibling;if(V!==null){V.return=a.return,Le=V;break}Le=a.return}}var ql=0,Zl=1,jl=2,Jl=3,Kl=4;if(typeof Symbol=="function"&&Symbol.for){var na=Symbol.for;ql=na("selector.component"),Zl=na("selector.has_pseudo_class"),jl=na("selector.role"),Jl=na("selector.test_id"),Kl=na("selector.text")}function vf(o){var a=z(o);if(a!=null){if(typeof a.memoizedProps["data-testname"]!="string")throw Error(l(364));return a}if(o=O(o),o===null)throw Error(l(362));return o.stateNode.current}function _f(o,a){switch(a.$$typeof){case ql:if(o.type===a.value)return!0;break;case Zl:e:{a=a.value,o=[o,0];for(var d=0;d<o.length;){var v=o[d++],S=o[d++],A=a[S];if(v.tag!==5||!re(v)){for(;A!=null&&_f(v,A);)S++,A=a[S];if(S===a.length){a=!0;break e}else for(v=v.child;v!==null;)o.push(v,S),v=v.sibling}}a=!1}return a;case jl:if(o.tag===5&&fe(o.stateNode,a.value))return!0;break;case Kl:if((o.tag===5||o.tag===6)&&(o=Z(o),o!==null&&0<=o.indexOf(a.value)))return!0;break;case Jl:if(o.tag===5&&(o=o.memoizedProps["data-testname"],typeof o=="string"&&o.toLowerCase()===a.value.toLowerCase()))return!0;break;default:throw Error(l(365))}return!1}function yf(o){switch(o.$$typeof){case ql:return"<"+(D(o.value)||"Unknown")+">";case Zl:return":has("+(yf(o)||"")+")";case jl:return'[role="'+o.value+'"]';case Kl:return'"'+o.value+'"';case Jl:return'[data-testname="'+o.value+'"]';default:throw Error(l(365))}}function hg(o,a){var d=[];o=[o,0];for(var v=0;v<o.length;){var S=o[v++],A=o[v++],B=a[A];if(S.tag!==5||!re(S)){for(;B!=null&&_f(S,B);)A++,B=a[A];if(A===a.length)d.push(S);else for(S=S.child;S!==null;)o.push(S,A),S=S.sibling}}return d}function xf(o,a){if(!Pe)throw Error(l(363));o=vf(o),o=hg(o,a),a=[],o=Array.from(o);for(var d=0;d<o.length;){var v=o[d++];if(v.tag===5)re(v)||a.push(v.stateNode);else for(v=v.child;v!==null;)o.push(v),v=v.sibling}return a}var wx=Math.ceil,Ql=c.ReactCurrentDispatcher,Sf=c.ReactCurrentOwner,$t=c.ReactCurrentBatchConfig,Tt=0,sn=null,on=null,xn=0,ni=0,Qs=Rt(0),ln=0,ia=null,$s=0,$l=0,Mf=0,ra=null,Wn=null,Ef=0,wf=1/0;function eo(){wf=pn()+500}var ec=!1,Tf=null,Ar=null,tc=!1,br=null,nc=0,sa=0,Af=null,ic=-1,rc=0;function Bn(){return Tt&6?pn():ic!==-1?ic:ic=pn()}function Cr(o){return o.mode&1?Tt&2&&xn!==0?xn&-xn:ox.transition!==null?(rc===0&&(o=vl,vl<<=1,!(vl&4194240)&&(vl=64),rc=o),rc):(o=Ut,o!==0?o:ve()):1}function di(o,a,d){if(50<sa)throw sa=0,Af=null,Error(l(185));var v=sc(o,a);return v===null?null:(Vo(v,a,d),(!(Tt&2)||v!==sn)&&(v===sn&&(!(Tt&2)&&($l|=a),ln===4&&Rr(v,xn)),Xn(v,d),a===1&&Tt===0&&!(o.mode&1)&&(eo(),Sl&&Oi())),v)}function sc(o,a){o.lanes|=a;var d=o.alternate;for(d!==null&&(d.lanes|=a),d=o,o=o.return;o!==null;)o.childLanes|=a,d=o.alternate,d!==null&&(d.childLanes|=a),d=o,o=o.return;return d.tag===3?d.stateNode:null}function Xn(o,a){var d=o.callbackNode;Ky(o,a);var v=yl(o,o===sn?xn:0);if(v===0)d!==null&&Kp(d),o.callbackNode=null,o.callbackPriority=0;else if(a=v&-v,o.callbackPriority!==a){if(d!=null&&Kp(d),a===1)o.tag===0?sx(dg.bind(null,o)):Qp(dg.bind(null,o)),Te?it(function(){Tt===0&&Oi()}):Dh(Uh,Oi),d=null;else{switch(Jp(v)){case 1:d=Uh;break;case 4:d=tx;break;case 16:d=Nh;break;case 536870912:d=nx;break;default:d=Nh}d=Mg(d,fg.bind(null,o))}o.callbackPriority=a,o.callbackNode=d}}function fg(o,a){if(ic=-1,rc=0,Tt&6)throw Error(l(327));var d=o.callbackNode;if(ts()&&o.callbackNode!==d)return null;var v=yl(o,o===sn?xn:0);if(v===0)return null;if(v&30||v&o.expiredLanes||a)a=oc(o,v);else{a=v;var S=Tt;Tt|=2;var A=gg();(sn!==o||xn!==a)&&(eo(),$r(o,a));do try{bx();break}catch(V){mg(o,V)}while(!0);Bh(),Ql.current=A,Tt=S,on!==null?a=0:(sn=null,xn=0,a=ln)}if(a!==0){if(a===2&&(S=Ph(o),S!==0&&(v=S,a=bf(o,S))),a===1)throw d=ia,$r(o,0),Rr(o,v),Xn(o,pn()),d;if(a===6)Rr(o,v);else{if(S=o.current.alternate,!(v&30)&&!Tx(S)&&(a=oc(o,v),a===2&&(A=Ph(o),A!==0&&(v=A,a=bf(o,A))),a===1))throw d=ia,$r(o,0),Rr(o,v),Xn(o,pn()),d;switch(o.finishedWork=S,o.finishedLanes=v,a){case 0:case 1:throw Error(l(345));case 2:es(o,Wn);break;case 3:if(Rr(o,v),(v&130023424)===v&&(a=Ef+500-pn(),10<a)){if(yl(o,0)!==0)break;if(S=o.suspendedLanes,(S&v)!==v){Bn(),o.pingedLanes|=o.suspendedLanes&S;break}o.timeoutHandle=we(es.bind(null,o,Wn),a);break}es(o,Wn);break;case 4:if(Rr(o,v),(v&4194240)===v)break;for(a=o.eventTimes,S=-1;0<v;){var B=31-Wt(v);A=1<<B,B=a[B],B>S&&(S=B),v&=~A}if(v=S,v=pn()-v,v=(120>v?120:480>v?480:1080>v?1080:1920>v?1920:3e3>v?3e3:4320>v?4320:1960*wx(v/1960))-v,10<v){o.timeoutHandle=we(es.bind(null,o,Wn),v);break}es(o,Wn);break;case 5:es(o,Wn);break;default:throw Error(l(329))}}}return Xn(o,pn()),o.callbackNode===d?fg.bind(null,o):null}function bf(o,a){var d=ra;return o.current.memoizedState.isDehydrated&&($r(o,a).flags|=256),o=oc(o,a),o!==2&&(a=Wn,Wn=d,a!==null&&Cf(a)),o}function Cf(o){Wn===null?Wn=o:Wn.push.apply(Wn,o)}function Tx(o){for(var a=o;;){if(a.flags&16384){var d=a.updateQueue;if(d!==null&&(d=d.stores,d!==null))for(var v=0;v<d.length;v++){var S=d[v],A=S.getSnapshot;S=S.value;try{if(!Ni(A(),S))return!1}catch{return!1}}}if(d=a.child,a.subtreeFlags&16384&&d!==null)d.return=a,a=d;else{if(a===o)break;for(;a.sibling===null;){if(a.return===null||a.return===o)return!0;a=a.return}a.sibling.return=a.return,a=a.sibling}}return!0}function Rr(o,a){for(a&=~Mf,a&=~$l,o.suspendedLanes|=a,o.pingedLanes&=~a,o=o.expirationTimes;0<a;){var d=31-Wt(a),v=1<<d;o[d]=-1,a&=~v}}function dg(o){if(Tt&6)throw Error(l(327));ts();var a=yl(o,0);if(!(a&1))return Xn(o,pn()),null;var d=oc(o,a);if(o.tag!==0&&d===2){var v=Ph(o);v!==0&&(a=v,d=bf(o,v))}if(d===1)throw d=ia,$r(o,0),Rr(o,a),Xn(o,pn()),d;if(d===6)throw Error(l(345));return o.finishedWork=o.current.alternate,o.finishedLanes=a,es(o,Wn),Xn(o,pn()),null}function pg(o){br!==null&&br.tag===0&&!(Tt&6)&&ts();var a=Tt;Tt|=1;var d=$t.transition,v=Ut;try{if($t.transition=null,Ut=1,o)return o()}finally{Ut=v,$t.transition=d,Tt=a,!(Tt&6)&&Oi()}}function Rf(){ni=Qs.current,at(Qs)}function $r(o,a){o.finishedWork=null,o.finishedLanes=0;var d=o.timeoutHandle;if(d!==lt&&(o.timeoutHandle=lt,et(d)),on!==null)for(d=on.return;d!==null;){var v=d;switch(Xh(v),v.tag){case 1:v=v.type.childContextTypes,v!=null&&dn();break;case 3:Js(),at(Gt),at(De),Qh();break;case 5:Jh(v);break;case 4:Js();break;case 13:at(Yt);break;case 19:at(Yt);break;case 10:zh(v.type._context);break;case 22:case 23:Rf()}d=d.return}if(sn=o,on=o=Pr(o.current,null),xn=ni=a,ln=0,ia=null,Mf=$l=$s=0,Wn=ra=null,Fi!==null){for(a=0;a<Fi.length;a++)if(d=Fi[a],v=d.interleaved,v!==null){d.interleaved=null;var S=v.next,A=d.pending;if(A!==null){var B=A.next;A.next=S,v.next=B}d.pending=v}Fi=null}return o}function mg(o,a){do{var d=on;try{if(Bh(),Ll.current=Bl,Dl){for(var v=Zt.memoizedState;v!==null;){var S=v.queue;S!==null&&(S.pending=null),v=v.next}Dl=!1}if(Ks=0,mn=An=Zt=null,Zo=!1,jo=0,Sf.current=null,d===null||d.return===null){ln=1,ia=a,on=null;break}e:{var A=o,B=d.return,V=d,ie=a;if(a=xn,V.flags|=32768,ie!==null&&typeof ie=="object"&&typeof ie.then=="function"){var Me=ie,Ge=V,pt=Ge.tag;if(!(Ge.mode&1)&&(pt===0||pt===11||pt===15)){var st=Ge.alternate;st?(Ge.updateQueue=st.updateQueue,Ge.memoizedState=st.memoizedState,Ge.lanes=st.lanes):(Ge.updateQueue=null,Ge.memoizedState=null)}var kt=Om(B);if(kt!==null){kt.flags&=-257,Fm(kt,B,V,A,a),kt.mode&1&&Nm(A,Me,a),a=kt,ie=Me;var $e=a.updateQueue;if($e===null){var Rn=new Set;Rn.add(ie),a.updateQueue=Rn}else $e.add(ie);break e}else{if(!(a&1)){Nm(A,Me,a),Pf();break e}ie=Error(l(426))}}else if(Xt&&V.mode&1){var mi=Om(B);if(mi!==null){!(mi.flags&65536)&&(mi.flags|=256),Fm(mi,B,V,A,a),Zh(ie);break e}}A=ie,ln!==4&&(ln=2),ra===null?ra=[A]:ra.push(A),ie=of(ie,V),V=B;do{switch(V.tag){case 3:V.flags|=65536,a&=-a,V.lanes|=a;var j=Dm(V,ie,a);tm(V,j);break e;case 1:A=ie;var W=V.type,ne=V.stateNode;if(!(V.flags&128)&&(typeof W.getDerivedStateFromError=="function"||ne!==null&&typeof ne.componentDidCatch=="function"&&(Ar===null||!Ar.has(ne)))){V.flags|=65536,a&=-a,V.lanes|=a;var Ne=Um(V,A,a);tm(V,Ne);break e}}V=V.return}while(V!==null)}_g(d)}catch(Ke){a=Ke,on===d&&d!==null&&(on=d=d.return);continue}break}while(!0)}function gg(){var o=Ql.current;return Ql.current=Bl,o===null?Bl:o}function Pf(){(ln===0||ln===3||ln===2)&&(ln=4),sn===null||!($s&268435455)&&!($l&268435455)||Rr(sn,xn)}function oc(o,a){var d=Tt;Tt|=2;var v=gg();sn===o&&xn===a||$r(o,a);do try{Ax();break}catch(S){mg(o,S)}while(!0);if(Bh(),Tt=d,Ql.current=v,on!==null)throw Error(l(261));return sn=null,xn=0,ln}function Ax(){for(;on!==null;)vg(on)}function bx(){for(;on!==null&&!$y();)vg(on)}function vg(o){var a=Sg(o.alternate,o,ni);o.memoizedProps=o.pendingProps,a===null?_g(o):on=a,Sf.current=null}function _g(o){var a=o;do{var d=a.alternate;if(o=a.return,a.flags&32768){if(d=yx(d,a),d!==null){d.flags&=32767,on=d;return}if(o!==null)o.flags|=32768,o.subtreeFlags=0,o.deletions=null;else{ln=6,on=null;return}}else if(d=gx(d,a,ni),d!==null){on=d;return}if(a=a.sibling,a!==null){on=a;return}on=a=o}while(a!==null);ln===0&&(ln=5)}function es(o,a){var d=Ut,v=$t.transition;try{$t.transition=null,Ut=1,Cx(o,a,d)}finally{$t.transition=v,Ut=d}return null}function Cx(o,a,d){do ts();while(br!==null);if(Tt&6)throw Error(l(327));var v=o.finishedWork,S=o.finishedLanes;if(v===null)return null;if(o.finishedWork=null,o.finishedLanes=0,v===o.current)throw Error(l(177));o.callbackNode=null,o.callbackPriority=0;var A=v.lanes|v.childLanes;if(Qy(o,A),o===sn&&(on=sn=null,xn=0),!(v.subtreeFlags&2064)&&!(v.flags&2064)||tc||(tc=!0,Mg(Nh,function(){return ts(),null})),A=(v.flags&15990)!==0,v.subtreeFlags&15990||A){A=$t.transition,$t.transition=null;var B=Ut;Ut=1;var V=Tt;Tt|=4,Sf.current=null,Sx(o,v),Mx(o,v),me(o.containerInfo),o.current=v,Ex(v),ex(),Tt=V,Ut=B,$t.transition=A}else o.current=v;if(tc&&(tc=!1,br=o,nc=S),A=o.pendingLanes,A===0&&(Ar=null),ix(v.stateNode),Xn(o,pn()),a!==null)for(d=o.onRecoverableError,v=0;v<a.length;v++)d(a[v]);if(ec)throw ec=!1,o=Tf,Tf=null,o;return nc&1&&o.tag!==0&&ts(),A=o.pendingLanes,A&1?o===Af?sa++:(sa=0,Af=o):sa=0,Oi(),null}function ts(){if(br!==null){var o=Jp(nc),a=$t.transition,d=Ut;try{if($t.transition=null,Ut=16>o?16:o,br===null)var v=!1;else{if(o=br,br=null,nc=0,Tt&6)throw Error(l(331));var S=Tt;for(Tt|=4,Le=o.current;Le!==null;){var A=Le,B=A.child;if(Le.flags&16){var V=A.deletions;if(V!==null){for(var ie=0;ie<V.length;ie++){var Me=V[ie];for(Le=Me;Le!==null;){var Ge=Le;switch(Ge.tag){case 0:case 11:case 15:Qr(8,Ge,A)}var pt=Ge.child;if(pt!==null)pt.return=Ge,Le=pt;else for(;Le!==null;){Ge=Le;var st=Ge.sibling,kt=Ge.return;if(ng(Ge),Ge===Me){Le=null;break}if(st!==null){st.return=kt,Le=st;break}Le=kt}}}var $e=A.alternate;if($e!==null){var Rn=$e.child;if(Rn!==null){$e.child=null;do{var mi=Rn.sibling;Rn.sibling=null,Rn=mi}while(Rn!==null)}}Le=A}}if(A.subtreeFlags&2064&&B!==null)B.return=A,Le=B;else e:for(;Le!==null;){if(A=Le,A.flags&2048)switch(A.tag){case 0:case 11:case 15:Qr(9,A,A.return)}var j=A.sibling;if(j!==null){j.return=A.return,Le=j;break e}Le=A.return}}var W=o.current;for(Le=W;Le!==null;){B=Le;var ne=B.child;if(B.subtreeFlags&2064&&ne!==null)ne.return=B,Le=ne;else e:for(B=W;Le!==null;){if(V=Le,V.flags&2048)try{switch(V.tag){case 0:case 11:case 15:ta(9,V)}}catch(Ke){Yn(V,V.return,Ke)}if(V===B){Le=null;break e}var Ne=V.sibling;if(Ne!==null){Ne.return=V.return,Le=Ne;break e}Le=V.return}}if(Tt=S,Oi(),Ui&&typeof Ui.onPostCommitFiberRoot=="function")try{Ui.onPostCommitFiberRoot(xl,o)}catch{}v=!0}return v}finally{Ut=d,$t.transition=a}}return!1}function yg(o,a,d){a=of(d,a),a=Dm(o,a,1),Tr(o,a),a=Bn(),o=sc(o,1),o!==null&&(Vo(o,1,a),Xn(o,a))}function Yn(o,a,d){if(o.tag===3)yg(o,o,d);else for(;a!==null;){if(a.tag===3){yg(a,o,d);break}else if(a.tag===1){var v=a.stateNode;if(typeof a.type.getDerivedStateFromError=="function"||typeof v.componentDidCatch=="function"&&(Ar===null||!Ar.has(v))){o=of(d,o),o=Um(a,o,1),Tr(a,o),o=Bn(),a=sc(a,1),a!==null&&(Vo(a,1,o),Xn(a,o));break}}a=a.return}}function Rx(o,a,d){var v=o.pingCache;v!==null&&v.delete(a),a=Bn(),o.pingedLanes|=o.suspendedLanes&d,sn===o&&(xn&d)===d&&(ln===4||ln===3&&(xn&130023424)===xn&&500>pn()-Ef?$r(o,0):Mf|=d),Xn(o,a)}function xg(o,a){a===0&&(o.mode&1?(a=_l,_l<<=1,!(_l&130023424)&&(_l=4194304)):a=1);var d=Bn();o=sc(o,a),o!==null&&(Vo(o,a,d),Xn(o,d))}function Px(o){var a=o.memoizedState,d=0;a!==null&&(d=a.retryLane),xg(o,d)}function Ix(o,a){var d=0;switch(o.tag){case 13:var v=o.stateNode,S=o.memoizedState;S!==null&&(d=S.retryLane);break;case 19:v=o.stateNode;break;default:throw Error(l(314))}v!==null&&v.delete(a),xg(o,d)}var Sg;Sg=function(o,a,d){if(o!==null)if(o.memoizedProps!==a.pendingProps||Gt.current)ti=!0;else{if(!(o.lanes&d)&&!(a.flags&128))return ti=!1,_x(o,a,d);ti=!!(o.flags&131072)}else ti=!1,Xt&&a.flags&1048576&&am(a,Rl,a.index);switch(a.lanes=0,a.tag){case 2:var v=a.type;o!==null&&(o.alternate=null,a.alternate=null,a.flags|=2),o=a.pendingProps;var S=fn(a,De.current);Ws(a,d),S=ef(null,a,v,o,S,d);var A=tf();return a.flags|=1,typeof S=="object"&&S!==null&&typeof S.render=="function"&&S.$$typeof===void 0?(a.tag=1,a.memoizedState=null,a.updateQueue=null,Qt(v)?(A=!0,On(a)):A=!1,a.memoizedState=S.state!==null&&S.state!==void 0?S.state:null,Hh(a),S.updater=bl,a.stateNode=S,S._reactInternals=a,Gh(a,v,o,d),a=cf(null,a,v,!0,A,d)):(a.tag=0,Xt&&A&&Wh(a),Fn(null,a,S,d),a=a.child),a;case 16:v=a.elementType;e:{switch(o!==null&&(o.alternate=null,a.alternate=null,a.flags|=2),o=a.pendingProps,S=v._init,v=S(v._payload),a.type=v,S=a.tag=Dx(v),o=yi(v,o),S){case 0:a=lf(null,a,v,o,d);break e;case 1:a=Xm(null,a,v,o,d);break e;case 11:a=km(null,a,v,o,d);break e;case 14:a=Hm(null,a,v,yi(v.type,o),d);break e}throw Error(l(306,v,""))}return a;case 0:return v=a.type,S=a.pendingProps,S=a.elementType===v?S:yi(v,S),lf(o,a,v,S,d);case 1:return v=a.type,S=a.pendingProps,S=a.elementType===v?S:yi(v,S),Xm(o,a,v,S,d);case 3:e:{if(Ym(a),o===null)throw Error(l(387));v=a.pendingProps,A=a.memoizedState,S=A.element,em(o,a),Al(a,v,null,d);var B=a.memoizedState;if(v=B.element,de&&A.isDehydrated)if(A={element:v,isDehydrated:!1,cache:B.cache,transitions:B.transitions},a.updateQueue.baseState=A,a.memoizedState=A,a.flags&256){S=Error(l(423)),a=qm(o,a,v,d,S);break e}else if(v!==S){S=Error(l(424)),a=qm(o,a,v,d,S);break e}else for(de&&(ei=fl(a.stateNode.containerInfo),$n=a,Xt=!0,xi=null,Go=!1),d=dm(a,null,v,d),a.child=d;d;)d.flags=d.flags&-3|4096,d=d.sibling;else{if(qs(),v===S){a=ir(o,a,d);break e}Fn(o,a,v,d)}a=a.child}return a;case 5:return pm(a),o===null&&qh(a),v=a.type,S=a.pendingProps,A=o!==null?o.memoizedProps:null,B=S.children,ge(v,S)?B=null:A!==null&&ge(v,A)&&(a.flags|=32),Wm(o,a),Fn(o,a,B,d),a.child;case 6:return o===null&&qh(a),null;case 13:return Zm(o,a,d);case 4:return jh(a,a.stateNode.containerInfo),v=a.pendingProps,o===null?a.child=Zs(a,null,v,d):Fn(o,a,v,d),a.child;case 11:return v=a.type,S=a.pendingProps,S=a.elementType===v?S:yi(v,S),km(o,a,v,S,d);case 7:return Fn(o,a,a.pendingProps,d),a.child;case 8:return Fn(o,a,a.pendingProps.children,d),a.child;case 12:return Fn(o,a,a.pendingProps.children,d),a.child;case 10:e:{if(v=a.type._context,S=a.pendingProps,A=a.memoizedProps,B=S.value,$p(a,v,B),A!==null)if(Ni(A.value,B)){if(A.children===S.children&&!Gt.current){a=ir(o,a,d);break e}}else for(A=a.child,A!==null&&(A.return=a);A!==null;){var V=A.dependencies;if(V!==null){B=A.child;for(var ie=V.firstContext;ie!==null;){if(ie.context===v){if(A.tag===1){ie=$i(-1,d&-d),ie.tag=2;var Me=A.updateQueue;if(Me!==null){Me=Me.shared;var Ge=Me.pending;Ge===null?ie.next=ie:(ie.next=Ge.next,Ge.next=ie),Me.pending=ie}}A.lanes|=d,ie=A.alternate,ie!==null&&(ie.lanes|=d),kh(A.return,d,a),V.lanes|=d;break}ie=ie.next}}else if(A.tag===10)B=A.type===a.type?null:A.child;else if(A.tag===18){if(B=A.return,B===null)throw Error(l(341));B.lanes|=d,V=B.alternate,V!==null&&(V.lanes|=d),kh(B,d,a),B=A.sibling}else B=A.child;if(B!==null)B.return=A;else for(B=A;B!==null;){if(B===a){B=null;break}if(A=B.sibling,A!==null){A.return=B.return,B=A;break}B=B.return}A=B}Fn(o,a,S.children,d),a=a.child}return a;case 9:return S=a.type,v=a.pendingProps.children,Ws(a,d),S=li(S),v=v(S),a.flags|=1,Fn(o,a,v,d),a.child;case 14:return v=a.type,S=yi(v,a.pendingProps),S=yi(v.type,S),Hm(o,a,v,S,d);case 15:return Vm(o,a,a.type,a.pendingProps,d);case 17:return v=a.type,S=a.pendingProps,S=a.elementType===v?S:yi(v,S),o!==null&&(o.alternate=null,a.alternate=null,a.flags|=2),a.tag=1,Qt(v)?(o=!0,On(a)):o=!1,Ws(a,d),sm(a,v,S),Gh(a,v,S,d),cf(null,a,v,!0,o,d);case 19:return Qm(o,a,d);case 22:return Gm(o,a,d)}throw Error(l(156,a.tag))};function Mg(o,a){return Dh(o,a)}function Lx(o,a,d,v){this.tag=o,this.key=d,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.ref=null,this.pendingProps=a,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=v,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function pi(o,a,d,v){return new Lx(o,a,d,v)}function If(o){return o=o.prototype,!(!o||!o.isReactComponent)}function Dx(o){if(typeof o=="function")return If(o)?1:0;if(o!=null){if(o=o.$$typeof,o===M)return 11;if(o===w)return 14}return 2}function Pr(o,a){var d=o.alternate;return d===null?(d=pi(o.tag,a,o.key,o.mode),d.elementType=o.elementType,d.type=o.type,d.stateNode=o.stateNode,d.alternate=o,o.alternate=d):(d.pendingProps=a,d.type=o.type,d.flags=0,d.subtreeFlags=0,d.deletions=null),d.flags=o.flags&14680064,d.childLanes=o.childLanes,d.lanes=o.lanes,d.child=o.child,d.memoizedProps=o.memoizedProps,d.memoizedState=o.memoizedState,d.updateQueue=o.updateQueue,a=o.dependencies,d.dependencies=a===null?null:{lanes:a.lanes,firstContext:a.firstContext},d.sibling=o.sibling,d.index=o.index,d.ref=o.ref,d}function ac(o,a,d,v,S,A){var B=2;if(v=o,typeof o=="function")If(o)&&(B=1);else if(typeof o=="string")B=5;else e:switch(o){case f:return ns(d.children,S,A,a);case p:B=8,S|=8;break;case m:return o=pi(12,d,a,S|2),o.elementType=m,o.lanes=A,o;case x:return o=pi(13,d,a,S),o.elementType=x,o.lanes=A,o;case _:return o=pi(19,d,a,S),o.elementType=_,o.lanes=A,o;case T:return lc(d,S,A,a);default:if(typeof o=="object"&&o!==null)switch(o.$$typeof){case g:B=10;break e;case y:B=9;break e;case M:B=11;break e;case w:B=14;break e;case E:B=16,v=null;break e}throw Error(l(130,o==null?o:typeof o,""))}return a=pi(B,d,a,S),a.elementType=o,a.type=v,a.lanes=A,a}function ns(o,a,d,v){return o=pi(7,o,v,a),o.lanes=d,o}function lc(o,a,d,v){return o=pi(22,o,v,a),o.elementType=T,o.lanes=d,o.stateNode={},o}function Lf(o,a,d){return o=pi(6,o,null,a),o.lanes=d,o}function Df(o,a,d){return a=pi(4,o.children!==null?o.children:[],o.key,a),a.lanes=d,a.stateNode={containerInfo:o.containerInfo,pendingChildren:null,implementation:o.implementation},a}function Ux(o,a,d,v,S){this.tag=a,this.containerInfo=o,this.finishedWork=this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=lt,this.callbackNode=this.pendingContext=this.context=null,this.callbackPriority=0,this.eventTimes=Ih(0),this.expirationTimes=Ih(-1),this.entangledLanes=this.finishedLanes=this.mutableReadLanes=this.expiredLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Ih(0),this.identifierPrefix=v,this.onRecoverableError=S,de&&(this.mutableSourceEagerHydrationData=null)}function Eg(o,a,d,v,S,A,B,V,ie){return o=new Ux(o,a,d,V,ie),a===1?(a=1,A===!0&&(a|=8)):a=0,A=pi(3,null,null,a),o.current=A,A.stateNode=o,A.memoizedState={element:v,isDehydrated:d,cache:null,transitions:null},Hh(A),o}function wg(o){if(!o)return wt;o=o._reactInternals;e:{if(C(o)!==o||o.tag!==1)throw Error(l(170));var a=o;do{switch(a.tag){case 3:a=a.stateNode.context;break e;case 1:if(Qt(a.type)){a=a.stateNode.__reactInternalMemoizedMergedChildContext;break e}}a=a.return}while(a!==null);throw Error(l(171))}if(o.tag===1){var d=o.type;if(Qt(d))return Bt(o,d,a)}return a}function Tg(o){var a=o._reactInternals;if(a===void 0)throw typeof o.render=="function"?Error(l(188)):(o=Object.keys(o).join(","),Error(l(268,o)));return o=q(a),o===null?null:o.stateNode}function Ag(o,a){if(o=o.memoizedState,o!==null&&o.dehydrated!==null){var d=o.retryLane;o.retryLane=d!==0&&d<a?d:a}}function Uf(o,a){Ag(o,a),(o=o.alternate)&&Ag(o,a)}function Nx(o){return o=q(o),o===null?null:o.stateNode}function Ox(){return null}return t.attemptContinuousHydration=function(o){if(o.tag===13){var a=Bn();di(o,134217728,a),Uf(o,134217728)}},t.attemptHydrationAtCurrentPriority=function(o){if(o.tag===13){var a=Bn(),d=Cr(o);di(o,d,a),Uf(o,d)}},t.attemptSynchronousHydration=function(o){switch(o.tag){case 3:var a=o.stateNode;if(a.current.memoizedState.isDehydrated){var d=Ho(a.pendingLanes);d!==0&&(Lh(a,d|1),Xn(a,pn()),!(Tt&6)&&(eo(),Oi()))}break;case 13:var v=Bn();pg(function(){return di(o,1,v)}),Uf(o,1)}},t.batchedUpdates=function(o,a){var d=Tt;Tt|=1;try{return o(a)}finally{Tt=d,Tt===0&&(eo(),Sl&&Oi())}},t.createComponentSelector=function(o){return{$$typeof:ql,value:o}},t.createContainer=function(o,a,d,v,S,A,B){return Eg(o,a,!1,null,d,v,S,A,B)},t.createHasPseudoClassSelector=function(o){return{$$typeof:Zl,value:o}},t.createHydrationContainer=function(o,a,d,v,S,A,B,V,ie){return o=Eg(d,v,!0,o,S,A,B,V,ie),o.context=wg(null),d=o.current,v=Bn(),S=Cr(d),A=$i(v,S),A.callback=a??null,Tr(d,A),o.current.lanes=S,Vo(o,S,v),Xn(o,v),o},t.createPortal=function(o,a,d){var v=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:h,key:v==null?null:""+v,children:o,containerInfo:a,implementation:d}},t.createRoleSelector=function(o){return{$$typeof:jl,value:o}},t.createTestNameSelector=function(o){return{$$typeof:Jl,value:o}},t.createTextSelector=function(o){return{$$typeof:Kl,value:o}},t.deferredUpdates=function(o){var a=Ut,d=$t.transition;try{return $t.transition=null,Ut=16,o()}finally{Ut=a,$t.transition=d}},t.discreteUpdates=function(o,a,d,v,S){var A=Ut,B=$t.transition;try{return $t.transition=null,Ut=1,o(a,d,v,S)}finally{Ut=A,$t.transition=B,Tt===0&&eo()}},t.findAllNodes=xf,t.findBoundingRects=function(o,a){if(!Pe)throw Error(l(363));a=xf(o,a),o=[];for(var d=0;d<a.length;d++)o.push(R(a[d]));for(a=o.length-1;0<a;a--){d=o[a];for(var v=d.x,S=v+d.width,A=d.y,B=A+d.height,V=a-1;0<=V;V--)if(a!==V){var ie=o[V],Me=ie.x,Ge=Me+ie.width,pt=ie.y,st=pt+ie.height;if(v>=Me&&A>=pt&&S<=Ge&&B<=st){o.splice(a,1);break}else if(v!==Me||d.width!==ie.width||st<A||pt>B){if(!(A!==pt||d.height!==ie.height||Ge<v||Me>S)){Me>v&&(ie.width+=Me-v,ie.x=v),Ge<S&&(ie.width=S-Me),o.splice(a,1);break}}else{pt>A&&(ie.height+=pt-A,ie.y=A),st<B&&(ie.height=B-pt),o.splice(a,1);break}}}return o},t.findHostInstance=Tg,t.findHostInstanceWithNoPortals=function(o){return o=N(o),o=o!==null?K(o):null,o===null?null:o.stateNode},t.findHostInstanceWithWarning=function(o){return Tg(o)},t.flushControlled=function(o){var a=Tt;Tt|=1;var d=$t.transition,v=Ut;try{$t.transition=null,Ut=1,o()}finally{Ut=v,$t.transition=d,Tt=a,Tt===0&&(eo(),Oi())}},t.flushPassiveEffects=ts,t.flushSync=pg,t.focusWithin=function(o,a){if(!Pe)throw Error(l(363));for(o=vf(o),a=hg(o,a),a=Array.from(a),o=0;o<a.length;){var d=a[o++];if(!re(d)){if(d.tag===5&&ce(d.stateNode))return!0;for(d=d.child;d!==null;)a.push(d),d=d.sibling}}return!1},t.getCurrentUpdatePriority=function(){return Ut},t.getFindAllNodesFailureDescription=function(o,a){if(!Pe)throw Error(l(363));var d=0,v=[];o=[vf(o),0];for(var S=0;S<o.length;){var A=o[S++],B=o[S++],V=a[B];if((A.tag!==5||!re(A))&&(_f(A,V)&&(v.push(yf(V)),B++,B>d&&(d=B)),B<a.length))for(A=A.child;A!==null;)o.push(A,B),A=A.sibling}if(d<a.length){for(o=[];d<a.length;d++)o.push(yf(a[d]));return`findAllNodes was able to match part of the selector:
  `+(v.join(" > ")+`

No matching component was found for:
  `)+o.join(" > ")}return null},t.getPublicRootInstance=function(o){if(o=o.current,!o.child)return null;switch(o.child.tag){case 5:return $(o.child.stateNode);default:return o.child.stateNode}},t.injectIntoDevTools=function(o){if(o={bundleType:o.bundleType,version:o.version,rendererPackageName:o.rendererPackageName,rendererConfig:o.rendererConfig,overrideHookState:null,overrideHookStateDeletePath:null,overrideHookStateRenamePath:null,overrideProps:null,overridePropsDeletePath:null,overridePropsRenamePath:null,setErrorHandler:null,setSuspenseHandler:null,scheduleUpdate:null,currentDispatcherRef:c.ReactCurrentDispatcher,findHostInstanceByFiber:Nx,findFiberByHostInstance:o.findFiberByHostInstance||Ox,findHostInstancesForRefresh:null,scheduleRefresh:null,scheduleRoot:null,setRefreshHandler:null,getCurrentFiber:null,reconcilerVersion:"18.0.0-fc46dba67-20220329"},typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u")o=!1;else{var a=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(a.isDisabled||!a.supportsFiber)o=!0;else{try{xl=a.inject(o),Ui=a}catch{}o=!!a.checkDCE}}return o},t.isAlreadyRendering=function(){return!1},t.observeVisibleRects=function(o,a,d,v){if(!Pe)throw Error(l(363));o=xf(o,a);var S=We(o,d,v).disconnect;return{disconnect:function(){S()}}},t.registerMutableSourceForHydration=function(o,a){var d=a._getVersion;d=d(a._source),o.mutableSourceEagerHydrationData==null?o.mutableSourceEagerHydrationData=[a,d]:o.mutableSourceEagerHydrationData.push(a,d)},t.runWithPriority=function(o,a){var d=Ut;try{return Ut=o,a()}finally{Ut=d}},t.shouldError=function(){return null},t.shouldSuspend=function(){return!1},t.updateContainer=function(o,a,d,v){var S=a.current,A=Bn(),B=Cr(S);return d=wg(d),a.context===null?a.context=d:a.pendingContext=d,a=$i(A,B),a.payload={element:o},v=v===void 0?null:v,v!==null&&(a.callback=v),Tr(S,a),o=di(S,B,A),o!==null&&Tl(o,S,B),B},t};Ry.exports=Yb;var qb=Ry.exports;const Zb=Bx(qb),Yp={},jb=r=>void Object.assign(Yp,r);function Jb(r,e){function t(f,{args:p=[],attach:m,...g},y){let M=`${f[0].toUpperCase()}${f.slice(1)}`,x;if(f==="primitive"){if(g.object===void 0)throw new Error("R3F: Primitives without 'object' are invalid!");const _=g.object;x=Mo(_,{type:f,root:y,attach:m,primitive:!0})}else{const _=Yp[M];if(!_)throw new Error(`R3F: ${M} is not part of the THREE namespace! Did you forget to extend? See: https://docs.pmnd.rs/react-three-fiber/api/objects#using-3rd-party-objects-declaratively`);if(!Array.isArray(p))throw new Error("R3F: The args prop must be an array!");x=Mo(new _(...p),{type:f,root:y,attach:m,memoizedProps:{args:p}})}return x.__r3f.attach===void 0&&(x.isBufferGeometry?x.__r3f.attach="geometry":x.isMaterial&&(x.__r3f.attach="material")),M!=="inject"&&Td(x,g),x}function n(f,p){let m=!1;if(p){var g,y;(g=p.__r3f)!=null&&g.attach?wd(f,p,p.__r3f.attach):p.isObject3D&&f.isObject3D&&(f.add(p),m=!0),m||(y=f.__r3f)==null||y.objects.push(p),p.__r3f||Mo(p,{}),p.__r3f.parent=f,ep(p),Eo(p)}}function i(f,p,m){let g=!1;if(p){var y,M;if((y=p.__r3f)!=null&&y.attach)wd(f,p,p.__r3f.attach);else if(p.isObject3D&&f.isObject3D){p.parent=f,p.dispatchEvent({type:"added"}),f.dispatchEvent({type:"childadded",child:p});const x=f.children.filter(w=>w!==p),_=x.indexOf(m);f.children=[...x.slice(0,_),p,...x.slice(_)],g=!0}g||(M=f.__r3f)==null||M.objects.push(p),p.__r3f||Mo(p,{}),p.__r3f.parent=f,ep(p),Eo(p)}}function s(f,p,m=!1){f&&[...f].forEach(g=>l(p,g,m))}function l(f,p,m){if(p){var g,y,M;if(p.__r3f&&(p.__r3f.parent=null),(g=f.__r3f)!=null&&g.objects&&(f.__r3f.objects=f.__r3f.objects.filter(T=>T!==p)),(y=p.__r3f)!=null&&y.attach)fv(f,p,p.__r3f.attach);else if(p.isObject3D&&f.isObject3D){var x;f.remove(p),(x=p.__r3f)!=null&&x.root&&iC(lu(p),p)}const w=(M=p.__r3f)==null?void 0:M.primitive,E=!w&&(m===void 0?p.dispose!==null:m);if(!w){var _;s((_=p.__r3f)==null?void 0:_.objects,p,E),s(p.children,p,E)}if(delete p.__r3f,E&&p.dispose&&p.type!=="Scene"){const T=()=>{try{p.dispose()}catch{}};typeof IS_REACT_ACT_ENVIRONMENT>"u"?Ud.unstable_scheduleCallback(Ud.unstable_IdlePriority,T):T()}Eo(f)}}function c(f,p,m,g){var y;const M=(y=f.__r3f)==null?void 0:y.parent;if(!M)return;const x=t(p,m,f.__r3f.root);if(f.children){for(const _ of f.children)_.__r3f&&n(x,_);f.children=f.children.filter(_=>!_.__r3f)}f.__r3f.objects.forEach(_=>n(x,_)),f.__r3f.objects=[],f.__r3f.autoRemovedBeforeAppend||l(M,f),x.parent&&(x.__r3f.autoRemovedBeforeAppend=!0),n(M,x),x.raycast&&x.__r3f.eventCount&&lu(x).getState().internal.interaction.push(x),[g,g.alternate].forEach(_=>{_!==null&&(_.stateNode=x,_.ref&&(typeof _.ref=="function"?_.ref(x):_.ref.current=x))})}const u=()=>{};return{reconciler:Zb({createInstance:t,removeChild:l,appendChild:n,appendInitialChild:n,insertBefore:i,supportsMutation:!0,isPrimaryRenderer:!1,supportsPersistence:!1,supportsHydration:!1,noTimeout:-1,appendChildToContainer:(f,p)=>{if(!p)return;const m=f.getState().scene;m.__r3f&&(m.__r3f.root=f,n(m,p))},removeChildFromContainer:(f,p)=>{p&&l(f.getState().scene,p)},insertInContainerBefore:(f,p,m)=>{if(!p||!m)return;const g=f.getState().scene;g.__r3f&&i(g,p,m)},getRootHostContext:()=>null,getChildHostContext:f=>f,finalizeInitialChildren(f){var p;return!!((p=f==null?void 0:f.__r3f)!=null?p:{}).handlers},prepareUpdate(f,p,m,g){var y;if(((y=f==null?void 0:f.__r3f)!=null?y:{}).primitive&&g.object&&g.object!==f)return[!0];{const{args:x=[],children:_,...w}=g,{args:E=[],children:T,...U}=m;if(!Array.isArray(x))throw new Error("R3F: the args prop must be an array!");if(x.some((D,F)=>D!==E[F]))return[!0];const P=Oy(f,w,U,!0);return P.changes.length?[!1,P]:null}},commitUpdate(f,[p,m],g,y,M,x){p?c(f,g,M,x):Td(f,m)},commitMount(f,p,m,g){var y;const M=(y=f.__r3f)!=null?y:{};f.raycast&&M.handlers&&M.eventCount&&lu(f).getState().internal.interaction.push(f)},getPublicInstance:f=>f,prepareForCommit:()=>null,preparePortalMount:f=>Mo(f.getState().scene),resetAfterCommit:()=>{},shouldSetTextContent:()=>!1,clearContainer:()=>!1,hideInstance(f){var p;const{attach:m,parent:g}=(p=f.__r3f)!=null?p:{};m&&g&&fv(g,f,m),f.isObject3D&&(f.visible=!1),Eo(f)},unhideInstance(f,p){var m;const{attach:g,parent:y}=(m=f.__r3f)!=null?m:{};g&&y&&wd(y,f,g),(f.isObject3D&&p.visible==null||p.visible)&&(f.visible=!0),Eo(f)},createTextInstance:u,hideTextInstance:u,unhideTextInstance:u,getCurrentEventPriority:()=>e?e():Ro.DefaultEventPriority,beforeActiveInstanceBlur:()=>{},afterActiveInstanceBlur:()=>{},detachDeletedInstance:()=>{},now:typeof performance<"u"&&Vt.fun(performance.now)?performance.now:Vt.fun(Date.now)?Date.now:()=>0,scheduleTimeout:Vt.fun(setTimeout)?setTimeout:void 0,cancelTimeout:Vt.fun(clearTimeout)?clearTimeout:void 0}),applyProps:Td}}var lv,cv;const Ed=r=>"colorSpace"in r||"outputColorSpace"in r,Py=()=>{var r;return(r=Yp.ColorManagement)!=null?r:null},Iy=r=>r&&r.isOrthographicCamera,Kb=r=>r&&r.hasOwnProperty("current"),ll=typeof window<"u"&&((lv=window.document)!=null&&lv.createElement||((cv=window.navigator)==null?void 0:cv.product)==="ReactNative")?ke.useLayoutEffect:ke.useEffect;function Ly(r){const e=ke.useRef(r);return ll(()=>void(e.current=r),[r]),e}function Qb({set:r}){return ll(()=>(r(new Promise(()=>null)),()=>r(!1)),[r]),null}class Dy extends ke.Component{constructor(...e){super(...e),this.state={error:!1}}componentDidCatch(e){this.props.set(e)}render(){return this.state.error?null:this.props.children}}Dy.getDerivedStateFromError=()=>({error:!0});const Uy="__default",uv=new Map,$b=r=>r&&!!r.memoized&&!!r.changes;function Ny(r){var e;const t=typeof window<"u"?(e=window.devicePixelRatio)!=null?e:2:1;return Array.isArray(r)?Math.min(Math.max(r[0],t),r[1]):r}const _a=r=>{var e;return(e=r.__r3f)==null?void 0:e.root.getState()};function lu(r){let e=r.__r3f.root;for(;e.getState().previousRoot;)e=e.getState().previousRoot;return e}const Vt={obj:r=>r===Object(r)&&!Vt.arr(r)&&typeof r!="function",fun:r=>typeof r=="function",str:r=>typeof r=="string",num:r=>typeof r=="number",boo:r=>typeof r=="boolean",und:r=>r===void 0,arr:r=>Array.isArray(r),equ(r,e,{arrays:t="shallow",objects:n="reference",strict:i=!0}={}){if(typeof r!=typeof e||!!r!=!!e)return!1;if(Vt.str(r)||Vt.num(r)||Vt.boo(r))return r===e;const s=Vt.obj(r);if(s&&n==="reference")return r===e;const l=Vt.arr(r);if(l&&t==="reference")return r===e;if((l||s)&&r===e)return!0;let c;for(c in r)if(!(c in e))return!1;if(s&&t==="shallow"&&n==="shallow"){for(c in i?e:r)if(!Vt.equ(r[c],e[c],{strict:i,objects:"reference"}))return!1}else for(c in i?e:r)if(r[c]!==e[c])return!1;if(Vt.und(c)){if(l&&r.length===0&&e.length===0||s&&Object.keys(r).length===0&&Object.keys(e).length===0)return!0;if(r!==e)return!1}return!0}};function eC(r){r.dispose&&r.type!=="Scene"&&r.dispose();for(const e in r)e.dispose==null||e.dispose(),delete r[e]}function Mo(r,e){const t=r;return t.__r3f={type:"",root:null,previousAttach:null,memoizedProps:{},eventCount:0,handlers:{},objects:[],parent:null,...e},r}function $d(r,e){let t=r;if(e.includes("-")){const n=e.split("-"),i=n.pop();return t=n.reduce((s,l)=>s[l],r),{target:t,key:i}}else return{target:t,key:e}}const hv=/-\d+$/;function wd(r,e,t){if(Vt.str(t)){if(hv.test(t)){const s=t.replace(hv,""),{target:l,key:c}=$d(r,s);Array.isArray(l[c])||(l[c]=[])}const{target:n,key:i}=$d(r,t);e.__r3f.previousAttach=n[i],n[i]=e}else e.__r3f.previousAttach=t(r,e)}function fv(r,e,t){var n,i;if(Vt.str(t)){const{target:s,key:l}=$d(r,t),c=e.__r3f.previousAttach;c===void 0?delete s[l]:s[l]=c}else(n=e.__r3f)==null||n.previousAttach==null||n.previousAttach(r,e);(i=e.__r3f)==null||delete i.previousAttach}function Oy(r,{children:e,key:t,ref:n,...i},{children:s,key:l,ref:c,...u}={},h=!1){const f=r.__r3f,p=Object.entries(i),m=[];if(h){const y=Object.keys(u);for(let M=0;M<y.length;M++)i.hasOwnProperty(y[M])||p.unshift([y[M],Uy+"remove"])}p.forEach(([y,M])=>{var x;if((x=r.__r3f)!=null&&x.primitive&&y==="object"||Vt.equ(M,u[y]))return;if(/^on(Pointer|Click|DoubleClick|ContextMenu|Wheel)/.test(y))return m.push([y,M,!0,[]]);let _=[];y.includes("-")&&(_=y.split("-")),m.push([y,M,!1,_]);for(const w in i){const E=i[w];w.startsWith(`${y}-`)&&m.push([w,E,!1,w.split("-")])}});const g={...i};return f!=null&&f.memoizedProps&&f!=null&&f.memoizedProps.args&&(g.args=f.memoizedProps.args),f!=null&&f.memoizedProps&&f!=null&&f.memoizedProps.attach&&(g.attach=f.memoizedProps.attach),{memoized:g,changes:m}}function Td(r,e){var t;const n=r.__r3f,i=n==null?void 0:n.root,s=i==null||i.getState==null?void 0:i.getState(),{memoized:l,changes:c}=$b(e)?e:Oy(r,e),u=n==null?void 0:n.eventCount;r.__r3f&&(r.__r3f.memoizedProps=l);for(let m=0;m<c.length;m++){let[g,y,M,x]=c[m];if(Ed(r)){const T="srgb",U="srgb-linear";g==="encoding"?(g="colorSpace",y=y===3001?T:U):g==="outputEncoding"&&(g="outputColorSpace",y=y===3001?T:U)}let _=r,w=_[g];if(x.length&&(w=x.reduce((E,T)=>E[T],r),!(w&&w.set))){const[E,...T]=x.reverse();_=T.reverse().reduce((U,P)=>U[P],r),g=E}if(y===Uy+"remove")if(_.constructor){let E=uv.get(_.constructor);E||(E=new _.constructor,uv.set(_.constructor,E)),y=E[g]}else y=0;if(M&&n)y?n.handlers[g]=y:delete n.handlers[g],n.eventCount=Object.keys(n.handlers).length;else if(w&&w.set&&(w.copy||w instanceof Cs)){if(Array.isArray(y))w.fromArray?w.fromArray(y):w.set(...y);else if(w.copy&&y&&y.constructor&&w.constructor===y.constructor)w.copy(y);else if(y!==void 0){var h;const E=(h=w)==null?void 0:h.isColor;!E&&w.setScalar?w.setScalar(y):w instanceof Cs&&y instanceof Cs?w.mask=y.mask:w.set(y),!Py()&&s&&!s.linear&&E&&w.convertSRGBToLinear()}}else{var f;if(_[g]=y,(f=_[g])!=null&&f.isTexture&&_[g].format===Dn&&_[g].type===bi&&s){const E=_[g];Ed(E)&&Ed(s.gl)?E.colorSpace=s.gl.outputColorSpace:E.encoding=s.gl.outputEncoding}}Eo(r)}if(n&&n.parent&&r.raycast&&u!==n.eventCount){const m=lu(r).getState().internal,g=m.interaction.indexOf(r);g>-1&&m.interaction.splice(g,1),n.eventCount&&m.interaction.push(r)}return!(c.length===1&&c[0][0]==="onUpdate")&&c.length&&(t=r.__r3f)!=null&&t.parent&&ep(r),r}function Eo(r){var e,t;const n=(e=r.__r3f)==null||(t=e.root)==null||t.getState==null?void 0:t.getState();n&&n.internal.frames===0&&n.invalidate()}function ep(r){r.onUpdate==null||r.onUpdate(r)}function tC(r,e){r.manual||(Iy(r)?(r.left=e.width/-2,r.right=e.width/2,r.top=e.height/2,r.bottom=e.height/-2):r.aspect=e.width/e.height,r.updateProjectionMatrix(),r.updateMatrixWorld())}function eu(r){return(r.eventObject||r.object).uuid+"/"+r.index+r.instanceId}function nC(){var r;const e=typeof self<"u"&&self||typeof window<"u"&&window;if(!e)return Ro.DefaultEventPriority;switch((r=e.event)==null?void 0:r.type){case"click":case"contextmenu":case"dblclick":case"pointercancel":case"pointerdown":case"pointerup":return Ro.DiscreteEventPriority;case"pointermove":case"pointerout":case"pointerover":case"pointerenter":case"pointerleave":case"wheel":return Ro.ContinuousEventPriority;default:return Ro.DefaultEventPriority}}function Fy(r,e,t,n){const i=t.get(e);i&&(t.delete(e),t.size===0&&(r.delete(n),i.target.releasePointerCapture(n)))}function iC(r,e){const{internal:t}=r.getState();t.interaction=t.interaction.filter(n=>n!==e),t.initialHits=t.initialHits.filter(n=>n!==e),t.hovered.forEach((n,i)=>{(n.eventObject===e||n.object===e)&&t.hovered.delete(i)}),t.capturedMap.forEach((n,i)=>{Fy(t.capturedMap,e,n,i)})}function rC(r){function e(u){const{internal:h}=r.getState(),f=u.offsetX-h.initialClick[0],p=u.offsetY-h.initialClick[1];return Math.round(Math.sqrt(f*f+p*p))}function t(u){return u.filter(h=>["Move","Over","Enter","Out","Leave"].some(f=>{var p;return(p=h.__r3f)==null?void 0:p.handlers["onPointer"+f]}))}function n(u,h){const f=r.getState(),p=new Set,m=[],g=h?h(f.internal.interaction):f.internal.interaction;for(let _=0;_<g.length;_++){const w=_a(g[_]);w&&(w.raycaster.camera=void 0)}f.previousRoot||f.events.compute==null||f.events.compute(u,f);function y(_){const w=_a(_);if(!w||!w.events.enabled||w.raycaster.camera===null)return[];if(w.raycaster.camera===void 0){var E;w.events.compute==null||w.events.compute(u,w,(E=w.previousRoot)==null?void 0:E.getState()),w.raycaster.camera===void 0&&(w.raycaster.camera=null)}return w.raycaster.camera?w.raycaster.intersectObject(_,!0):[]}let M=g.flatMap(y).sort((_,w)=>{const E=_a(_.object),T=_a(w.object);return!E||!T?_.distance-w.distance:T.events.priority-E.events.priority||_.distance-w.distance}).filter(_=>{const w=eu(_);return p.has(w)?!1:(p.add(w),!0)});f.events.filter&&(M=f.events.filter(M,f));for(const _ of M){let w=_.object;for(;w;){var x;(x=w.__r3f)!=null&&x.eventCount&&m.push({..._,eventObject:w}),w=w.parent}}if("pointerId"in u&&f.internal.capturedMap.has(u.pointerId))for(let _ of f.internal.capturedMap.get(u.pointerId).values())p.has(eu(_.intersection))||m.push(_.intersection);return m}function i(u,h,f,p){const m=r.getState();if(u.length){const g={stopped:!1};for(const y of u){const M=_a(y.object)||m,{raycaster:x,pointer:_,camera:w,internal:E}=M,T=new L(_.x,_.y,0).unproject(w),U=b=>{var N,q;return(N=(q=E.capturedMap.get(b))==null?void 0:q.has(y.eventObject))!=null?N:!1},P=b=>{const N={intersection:y,target:h.target};E.capturedMap.has(b)?E.capturedMap.get(b).set(y.eventObject,N):E.capturedMap.set(b,new Map([[y.eventObject,N]])),h.target.setPointerCapture(b)},D=b=>{const N=E.capturedMap.get(b);N&&Fy(E.capturedMap,y.eventObject,N,b)};let F={};for(let b in h){let N=h[b];typeof N!="function"&&(F[b]=N)}let C={...y,...F,pointer:_,intersections:u,stopped:g.stopped,delta:f,unprojectedPoint:T,ray:x.ray,camera:w,stopPropagation(){const b="pointerId"in h&&E.capturedMap.get(h.pointerId);if((!b||b.has(y.eventObject))&&(C.stopped=g.stopped=!0,E.hovered.size&&Array.from(E.hovered.values()).find(N=>N.eventObject===y.eventObject))){const N=u.slice(0,u.indexOf(y));s([...N,y])}},target:{hasPointerCapture:U,setPointerCapture:P,releasePointerCapture:D},currentTarget:{hasPointerCapture:U,setPointerCapture:P,releasePointerCapture:D},nativeEvent:h};if(p(C),g.stopped===!0)break}}return u}function s(u){const{internal:h}=r.getState();for(const f of h.hovered.values())if(!u.length||!u.find(p=>p.object===f.object&&p.index===f.index&&p.instanceId===f.instanceId)){const m=f.eventObject.__r3f,g=m==null?void 0:m.handlers;if(h.hovered.delete(eu(f)),m!=null&&m.eventCount){const y={...f,intersections:u};g.onPointerOut==null||g.onPointerOut(y),g.onPointerLeave==null||g.onPointerLeave(y)}}}function l(u,h){for(let f=0;f<h.length;f++){const p=h[f].__r3f;p==null||p.handlers.onPointerMissed==null||p.handlers.onPointerMissed(u)}}function c(u){switch(u){case"onPointerLeave":case"onPointerCancel":return()=>s([]);case"onLostPointerCapture":return h=>{const{internal:f}=r.getState();"pointerId"in h&&f.capturedMap.has(h.pointerId)&&requestAnimationFrame(()=>{f.capturedMap.has(h.pointerId)&&(f.capturedMap.delete(h.pointerId),s([]))})}}return function(f){const{onPointerMissed:p,internal:m}=r.getState();m.lastEvent.current=f;const g=u==="onPointerMove",y=u==="onClick"||u==="onContextMenu"||u==="onDoubleClick",x=n(f,g?t:void 0),_=y?e(f):0;u==="onPointerDown"&&(m.initialClick=[f.offsetX,f.offsetY],m.initialHits=x.map(E=>E.eventObject)),y&&!x.length&&_<=2&&(l(f,m.interaction),p&&p(f)),g&&s(x);function w(E){const T=E.eventObject,U=T.__r3f,P=U==null?void 0:U.handlers;if(U!=null&&U.eventCount)if(g){if(P.onPointerOver||P.onPointerEnter||P.onPointerOut||P.onPointerLeave){const D=eu(E),F=m.hovered.get(D);F?F.stopped&&E.stopPropagation():(m.hovered.set(D,E),P.onPointerOver==null||P.onPointerOver(E),P.onPointerEnter==null||P.onPointerEnter(E))}P.onPointerMove==null||P.onPointerMove(E)}else{const D=P[u];D?(!y||m.initialHits.includes(T))&&(l(f,m.interaction.filter(F=>!m.initialHits.includes(F))),D(E)):y&&m.initialHits.includes(T)&&l(f,m.interaction.filter(F=>!m.initialHits.includes(F)))}}i(x,f,_,w)}}return{handlePointer:c}}const By=r=>!!(r!=null&&r.render),zy=ke.createContext(null),sC=(r,e)=>{const t=Xb((c,u)=>{const h=new L,f=new L,p=new L;function m(_=u().camera,w=f,E=u().size){const{width:T,height:U,top:P,left:D}=E,F=T/U;w.isVector3?p.copy(w):p.set(...w);const C=_.getWorldPosition(h).distanceTo(p);if(Iy(_))return{width:T/_.zoom,height:U/_.zoom,top:P,left:D,factor:1,distance:C,aspect:F};{const b=_.fov*Math.PI/180,N=2*Math.tan(b/2)*C,q=N*(T/U);return{width:q,height:N,top:P,left:D,factor:T/q,distance:C,aspect:F}}}let g;const y=_=>c(w=>({performance:{...w.performance,current:_}})),M=new ae;return{set:c,get:u,gl:null,camera:null,raycaster:null,events:{priority:1,enabled:!0,connected:!1},xr:null,scene:null,invalidate:(_=1)=>r(u(),_),advance:(_,w)=>e(_,w,u()),legacy:!1,linear:!1,flat:!1,controls:null,clock:new Hp,pointer:M,mouse:M,frameloop:"always",onPointerMissed:void 0,performance:{current:1,min:.5,max:1,debounce:200,regress:()=>{const _=u();g&&clearTimeout(g),_.performance.current!==_.performance.min&&y(_.performance.min),g=setTimeout(()=>y(u().performance.max),_.performance.debounce)}},size:{width:0,height:0,top:0,left:0,updateStyle:!1},viewport:{initialDpr:0,dpr:0,width:0,height:0,top:0,left:0,aspect:0,distance:0,factor:0,getCurrentViewport:m},setEvents:_=>c(w=>({...w,events:{...w.events,..._}})),setSize:(_,w,E,T,U)=>{const P=u().camera,D={width:_,height:w,top:T||0,left:U||0,updateStyle:E};c(F=>({size:D,viewport:{...F.viewport,...m(P,f,D)}}))},setDpr:_=>c(w=>{const E=Ny(_);return{viewport:{...w.viewport,dpr:E,initialDpr:w.viewport.initialDpr||E}}}),setFrameloop:(_="always")=>{const w=u().clock;w.stop(),w.elapsedTime=0,_!=="never"&&(w.start(),w.elapsedTime=0),c(()=>({frameloop:_}))},previousRoot:void 0,internal:{active:!1,priority:0,frames:0,lastEvent:ke.createRef(),interaction:[],hovered:new Map,subscribers:[],initialClick:[0,0],initialHits:[],capturedMap:new Map,subscribe:(_,w,E)=>{const T=u().internal;return T.priority=T.priority+(w>0?1:0),T.subscribers.push({ref:_,priority:w,store:E}),T.subscribers=T.subscribers.sort((U,P)=>U.priority-P.priority),()=>{const U=u().internal;U!=null&&U.subscribers&&(U.priority=U.priority-(w>0?1:0),U.subscribers=U.subscribers.filter(P=>P.ref!==_))}}}}}),n=t.getState();let i=n.size,s=n.viewport.dpr,l=n.camera;return t.subscribe(()=>{const{camera:c,size:u,viewport:h,gl:f,set:p}=t.getState();if(u.width!==i.width||u.height!==i.height||h.dpr!==s){var m;i=u,s=h.dpr,tC(c,u),f.setPixelRatio(h.dpr);const g=(m=u.updateStyle)!=null?m:typeof HTMLCanvasElement<"u"&&f.domElement instanceof HTMLCanvasElement;f.setSize(u.width,u.height,g)}c!==l&&(l=c,p(g=>({viewport:{...g.viewport,...g.viewport.getCurrentViewport(c)}})))}),t.subscribe(c=>r(c)),t};let tu,oC=new Set,aC=new Set,lC=new Set;function Ad(r,e){if(r.size)for(const{callback:t}of r.values())t(e)}function ya(r,e){switch(r){case"before":return Ad(oC,e);case"after":return Ad(aC,e);case"tail":return Ad(lC,e)}}let bd,Cd;function Rd(r,e,t){let n=e.clock.getDelta();for(e.frameloop==="never"&&typeof r=="number"&&(n=r-e.clock.elapsedTime,e.clock.oldTime=e.clock.elapsedTime,e.clock.elapsedTime=r),bd=e.internal.subscribers,tu=0;tu<bd.length;tu++)Cd=bd[tu],Cd.ref.current(Cd.store.getState(),n,t);return!e.internal.priority&&e.gl.render&&e.gl.render(e.scene,e.camera),e.internal.frames=Math.max(0,e.internal.frames-1),e.frameloop==="always"?1:e.internal.frames}function cC(r){let e=!1,t=!1,n,i,s;function l(h){i=requestAnimationFrame(l),e=!0,n=0,ya("before",h),t=!0;for(const p of r.values()){var f;s=p.store.getState(),s.internal.active&&(s.frameloop==="always"||s.internal.frames>0)&&!((f=s.gl.xr)!=null&&f.isPresenting)&&(n+=Rd(h,s))}if(t=!1,ya("after",h),n===0)return ya("tail",h),e=!1,cancelAnimationFrame(i)}function c(h,f=1){var p;if(!h)return r.forEach(m=>c(m.store.getState(),f));(p=h.gl.xr)!=null&&p.isPresenting||!h.internal.active||h.frameloop==="never"||(f>1?h.internal.frames=Math.min(60,h.internal.frames+f):t?h.internal.frames=2:h.internal.frames=1,e||(e=!0,requestAnimationFrame(l)))}function u(h,f=!0,p,m){if(f&&ya("before",h),p)Rd(h,p,m);else for(const g of r.values())Rd(h,g.store.getState());f&&ya("after",h)}return{loop:l,invalidate:c,advance:u}}function ky(){const r=ke.useContext(zy);if(!r)throw new Error("R3F: Hooks can only be used within the Canvas component!");return r}function ur(r=t=>t,e){return ky()(r,e)}function uC(r,e=0){const t=ky(),n=t.getState().internal.subscribe,i=Ly(r);return ll(()=>n(i,e,t),[e,n,t]),null}const No=new Map,{invalidate:dv,advance:pv}=cC(No),{reconciler:Ju,applyProps:xo}=Jb(No,nC),So={objects:"shallow",strict:!1},hC=(r,e)=>{const t=typeof r=="function"?r(e):r;return By(t)?t:new U_({powerPreference:"high-performance",canvas:e,antialias:!0,alpha:!0,...r})};function fC(r,e){const t=typeof HTMLCanvasElement<"u"&&r instanceof HTMLCanvasElement;if(e){const{width:n,height:i,top:s,left:l,updateStyle:c=t}=e;return{width:n,height:i,top:s,left:l,updateStyle:c}}else if(typeof HTMLCanvasElement<"u"&&r instanceof HTMLCanvasElement&&r.parentElement){const{width:n,height:i,top:s,left:l}=r.parentElement.getBoundingClientRect();return{width:n,height:i,top:s,left:l,updateStyle:t}}else if(typeof OffscreenCanvas<"u"&&r instanceof OffscreenCanvas)return{width:r.width,height:r.height,top:0,left:0,updateStyle:t};return{width:0,height:0,top:0,left:0}}function dC(r){const e=No.get(r),t=e==null?void 0:e.fiber,n=e==null?void 0:e.store;e&&console.warn("R3F.createRoot should only be called once!");const i=typeof reportError=="function"?reportError:console.error,s=n||sC(dv,pv),l=t||Ju.createContainer(s,Ro.ConcurrentRoot,null,!1,null,"",i,null);e||No.set(r,{fiber:l,store:s});let c,u=!1,h;return{configure(f={}){let{gl:p,size:m,scene:g,events:y,onCreated:M,shadows:x=!1,linear:_=!1,flat:w=!1,legacy:E=!1,orthographic:T=!1,frameloop:U="always",dpr:P=[1,2],performance:D,raycaster:F,camera:C,onPointerMissed:b}=f,N=s.getState(),q=N.gl;N.gl||N.set({gl:q=hC(p,r)});let Y=N.raycaster;Y||N.set({raycaster:Y=new Ty});const{params:K,...le}=F||{};if(Vt.equ(le,Y,So)||xo(Y,{...le}),Vt.equ(K,Y.params,So)||xo(Y,{params:{...Y.params,...K}}),!N.camera||N.camera===h&&!Vt.equ(h,C,So)){h=C;const me=C instanceof el,Se=me?C:T?new kr(0,0,0,0,.1,1e3):new tn(75,0,.1,1e3);me||(Se.position.z=5,C&&(xo(Se,C),("aspect"in C||"left"in C||"right"in C||"bottom"in C||"top"in C)&&(Se.manual=!0,Se.updateProjectionMatrix())),!N.camera&&!(C!=null&&C.rotation)&&Se.lookAt(0,0,0)),N.set({camera:Se}),Y.camera=Se}if(!N.scene){let me;g!=null&&g.isScene?me=g:(me=new Mp,g&&xo(me,g)),N.set({scene:Mo(me)})}if(!N.xr){var $;const me=(Je,se)=>{const ge=s.getState();ge.frameloop!=="never"&&pv(Je,!0,ge,se)},Se=()=>{const Je=s.getState();Je.gl.xr.enabled=Je.gl.xr.isPresenting,Je.gl.xr.setAnimationLoop(Je.gl.xr.isPresenting?me:null),Je.gl.xr.isPresenting||dv(Je)},Qe={connect(){const Je=s.getState().gl;Je.xr.addEventListener("sessionstart",Se),Je.xr.addEventListener("sessionend",Se)},disconnect(){const Je=s.getState().gl;Je.xr.removeEventListener("sessionstart",Se),Je.xr.removeEventListener("sessionend",Se)}};typeof(($=q.xr)==null?void 0:$.addEventListener)=="function"&&Qe.connect(),N.set({xr:Qe})}if(q.shadowMap){const me=q.shadowMap.enabled,Se=q.shadowMap.type;if(q.shadowMap.enabled=!!x,Vt.boo(x))q.shadowMap.type=Ea;else if(Vt.str(x)){var pe;const Qe={basic:Iv,percentage:Ku,soft:Ea,variance:wi};q.shadowMap.type=(pe=Qe[x])!=null?pe:Ea}else Vt.obj(x)&&Object.assign(q.shadowMap,x);(me!==q.shadowMap.enabled||Se!==q.shadowMap.type)&&(q.shadowMap.needsUpdate=!0)}const J=Py();J&&("enabled"in J?J.enabled=!E:"legacyMode"in J&&(J.legacyMode=E)),u||xo(q,{outputEncoding:_?3e3:3001,toneMapping:w?qi:tp}),N.legacy!==E&&N.set(()=>({legacy:E})),N.linear!==_&&N.set(()=>({linear:_})),N.flat!==w&&N.set(()=>({flat:w})),p&&!Vt.fun(p)&&!By(p)&&!Vt.equ(p,q,So)&&xo(q,p),y&&!N.events.handlers&&N.set({events:y(s)});const xe=fC(r,m);return Vt.equ(xe,N.size,So)||N.setSize(xe.width,xe.height,xe.updateStyle,xe.top,xe.left),P&&N.viewport.dpr!==Ny(P)&&N.setDpr(P),N.frameloop!==U&&N.setFrameloop(U),N.onPointerMissed||N.set({onPointerMissed:b}),D&&!Vt.equ(D,N.performance,So)&&N.set(me=>({performance:{...me.performance,...D}})),c=M,u=!0,this},render(f){return u||this.configure(),Ju.updateContainer(Ti.jsx(pC,{store:s,children:f,onCreated:c,rootElement:r}),l,null,()=>{}),s},unmount(){Hy(r)}}}function pC({store:r,children:e,onCreated:t,rootElement:n}){return ll(()=>{const i=r.getState();i.set(s=>({internal:{...s.internal,active:!0}})),t&&t(i),r.getState().events.connected||i.events.connect==null||i.events.connect(n)},[]),Ti.jsx(zy.Provider,{value:r,children:e})}function Hy(r,e){const t=No.get(r),n=t==null?void 0:t.fiber;if(n){const i=t==null?void 0:t.store.getState();i&&(i.internal.active=!1),Ju.updateContainer(null,n,null,()=>{i&&setTimeout(()=>{try{var s,l,c,u;i.events.disconnect==null||i.events.disconnect(),(s=i.gl)==null||(l=s.renderLists)==null||l.dispose==null||l.dispose(),(c=i.gl)==null||c.forceContextLoss==null||c.forceContextLoss(),(u=i.gl)!=null&&u.xr&&i.xr.disconnect(),eC(i),No.delete(r)}catch{}},500)})}}Ju.injectIntoDevTools({bundleType:0,rendererPackageName:"@react-three/fiber",version:ke.version});const Pd={onClick:["click",!1],onContextMenu:["contextmenu",!1],onDoubleClick:["dblclick",!1],onWheel:["wheel",!0],onPointerDown:["pointerdown",!0],onPointerUp:["pointerup",!0],onPointerLeave:["pointerleave",!0],onPointerMove:["pointermove",!0],onPointerCancel:["pointercancel",!0],onLostPointerCapture:["lostpointercapture",!0]};function mC(r){const{handlePointer:e}=rC(r);return{priority:1,enabled:!0,compute(t,n,i){n.pointer.set(t.offsetX/n.size.width*2-1,-(t.offsetY/n.size.height)*2+1),n.raycaster.setFromCamera(n.pointer,n.camera)},connected:void 0,handlers:Object.keys(Pd).reduce((t,n)=>({...t,[n]:e(n)}),{}),update:()=>{var t;const{events:n,internal:i}=r.getState();(t=i.lastEvent)!=null&&t.current&&n.handlers&&n.handlers.onPointerMove(i.lastEvent.current)},connect:t=>{var n;const{set:i,events:s}=r.getState();s.disconnect==null||s.disconnect(),i(l=>({events:{...l.events,connected:t}})),Object.entries((n=s.handlers)!=null?n:[]).forEach(([l,c])=>{const[u,h]=Pd[l];t.addEventListener(u,c,{passive:h})})},disconnect:()=>{const{set:t,events:n}=r.getState();if(n.connected){var i;Object.entries((i=n.handlers)!=null?i:[]).forEach(([s,l])=>{if(n&&n.connected instanceof HTMLElement){const[c]=Pd[s];n.connected.removeEventListener(c,l)}}),t(s=>({events:{...s.events,connected:void 0}}))}}}}function mv(r,e){let t;return(...n)=>{window.clearTimeout(t),t=window.setTimeout(()=>r(...n),e)}}function gC({debounce:r,scroll:e,polyfill:t,offsetSize:n}={debounce:0,scroll:!1,offsetSize:!1}){const i=t||(typeof window>"u"?class{}:window.ResizeObserver);if(!i)throw new Error("This browser does not support ResizeObserver out of the box. See: https://github.com/react-spring/react-use-measure/#resize-observer-polyfills");const[s,l]=ke.useState({left:0,top:0,width:0,height:0,bottom:0,right:0,x:0,y:0}),c=ke.useRef({element:null,scrollContainers:null,resizeObserver:null,lastBounds:s,orientationHandler:null}),u=r?typeof r=="number"?r:r.scroll:null,h=r?typeof r=="number"?r:r.resize:null,f=ke.useRef(!1);ke.useEffect(()=>(f.current=!0,()=>void(f.current=!1)));const[p,m,g]=ke.useMemo(()=>{const _=()=>{if(!c.current.element)return;const{left:w,top:E,width:T,height:U,bottom:P,right:D,x:F,y:C}=c.current.element.getBoundingClientRect(),b={left:w,top:E,width:T,height:U,bottom:P,right:D,x:F,y:C};c.current.element instanceof HTMLElement&&n&&(b.height=c.current.element.offsetHeight,b.width=c.current.element.offsetWidth),Object.freeze(b),f.current&&!xC(c.current.lastBounds,b)&&l(c.current.lastBounds=b)};return[_,h?mv(_,h):_,u?mv(_,u):_]},[l,n,u,h]);function y(){c.current.scrollContainers&&(c.current.scrollContainers.forEach(_=>_.removeEventListener("scroll",g,!0)),c.current.scrollContainers=null),c.current.resizeObserver&&(c.current.resizeObserver.disconnect(),c.current.resizeObserver=null),c.current.orientationHandler&&("orientation"in screen&&"removeEventListener"in screen.orientation?screen.orientation.removeEventListener("change",c.current.orientationHandler):"onorientationchange"in window&&window.removeEventListener("orientationchange",c.current.orientationHandler))}function M(){c.current.element&&(c.current.resizeObserver=new i(g),c.current.resizeObserver.observe(c.current.element),e&&c.current.scrollContainers&&c.current.scrollContainers.forEach(_=>_.addEventListener("scroll",g,{capture:!0,passive:!0})),c.current.orientationHandler=()=>{g()},"orientation"in screen&&"addEventListener"in screen.orientation?screen.orientation.addEventListener("change",c.current.orientationHandler):"onorientationchange"in window&&window.addEventListener("orientationchange",c.current.orientationHandler))}const x=_=>{!_||_===c.current.element||(y(),c.current.element=_,c.current.scrollContainers=Vy(_),M())};return _C(g,!!e),vC(m),ke.useEffect(()=>{y(),M()},[e,g,m]),ke.useEffect(()=>y,[]),[x,s,p]}function vC(r){ke.useEffect(()=>{const e=r;return window.addEventListener("resize",e),()=>void window.removeEventListener("resize",e)},[r])}function _C(r,e){ke.useEffect(()=>{if(e){const t=r;return window.addEventListener("scroll",t,{capture:!0,passive:!0}),()=>void window.removeEventListener("scroll",t,!0)}},[r,e])}function Vy(r){const e=[];if(!r||r===document.body)return e;const{overflow:t,overflowX:n,overflowY:i}=window.getComputedStyle(r);return[t,n,i].some(s=>s==="auto"||s==="scroll")&&e.push(r),[...e,...Vy(r.parentElement)]}const yC=["x","y","top","bottom","left","right","width","height"],xC=(r,e)=>yC.every(t=>r[t]===e[t]);var SC=Object.defineProperty,MC=Object.defineProperties,EC=Object.getOwnPropertyDescriptors,gv=Object.getOwnPropertySymbols,wC=Object.prototype.hasOwnProperty,TC=Object.prototype.propertyIsEnumerable,vv=(r,e,t)=>e in r?SC(r,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):r[e]=t,_v=(r,e)=>{for(var t in e||(e={}))wC.call(e,t)&&vv(r,t,e[t]);if(gv)for(var t of gv(e))TC.call(e,t)&&vv(r,t,e[t]);return r},AC=(r,e)=>MC(r,EC(e)),yv,xv;typeof window<"u"&&((yv=window.document)!=null&&yv.createElement||((xv=window.navigator)==null?void 0:xv.product)==="ReactNative")?ke.useLayoutEffect:ke.useEffect;function Gy(r,e,t){if(!r)return;if(t(r)===!0)return r;let n=r.child;for(;n;){const i=Gy(n,e,t);if(i)return i;n=n.sibling}}function Wy(r){try{return Object.defineProperties(r,{_currentRenderer:{get(){return null},set(){}},_currentRenderer2:{get(){return null},set(){}}})}catch{return r}}const Sv=console.error;console.error=function(){const r=[...arguments].join("");if(r!=null&&r.startsWith("Warning:")&&r.includes("useContext")){console.error=Sv;return}return Sv.apply(this,arguments)};const qp=Wy(ke.createContext(null));class Xy extends ke.Component{render(){return ke.createElement(qp.Provider,{value:this._reactInternals},this.props.children)}}function bC(){const r=ke.useContext(qp);if(r===null)throw new Error("its-fine: useFiber must be called within a <FiberProvider />!");const e=ke.useId();return ke.useMemo(()=>{for(const n of[r,r==null?void 0:r.alternate]){if(!n)continue;const i=Gy(n,!1,s=>{let l=s.memoizedState;for(;l;){if(l.memoizedState===e)return!0;l=l.next}});if(i)return i}},[r,e])}function CC(){const r=bC(),[e]=ke.useState(()=>new Map);e.clear();let t=r;for(;t;){if(t.type&&typeof t.type=="object"){const i=t.type._context===void 0&&t.type.Provider===t.type?t.type:t.type._context;i&&i!==qp&&!e.has(i)&&e.set(i,ke.useContext(Wy(i)))}t=t.return}return e}function RC(){const r=CC();return ke.useMemo(()=>Array.from(r.keys()).reduce((e,t)=>n=>ke.createElement(e,null,ke.createElement(t.Provider,AC(_v({},n),{value:r.get(t)}))),e=>ke.createElement(Xy,_v({},e))),[r])}const PC=ke.forwardRef(function({children:e,fallback:t,resize:n,style:i,gl:s,events:l=mC,eventSource:c,eventPrefix:u,shadows:h,linear:f,flat:p,legacy:m,orthographic:g,frameloop:y,dpr:M,performance:x,raycaster:_,camera:w,scene:E,onPointerMissed:T,onCreated:U,...P},D){ke.useMemo(()=>jb(Vb),[]);const F=RC(),[C,b]=gC({scroll:!0,debounce:{scroll:50,resize:0},...n}),N=ke.useRef(null),q=ke.useRef(null);ke.useImperativeHandle(D,()=>N.current);const Y=Ly(T),[K,le]=ke.useState(!1),[$,pe]=ke.useState(!1);if(K)throw K;if($)throw $;const J=ke.useRef(null);ll(()=>{const me=N.current;b.width>0&&b.height>0&&me&&(J.current||(J.current=dC(me)),J.current.configure({gl:s,events:l,shadows:h,linear:f,flat:p,legacy:m,orthographic:g,frameloop:y,dpr:M,performance:x,raycaster:_,camera:w,scene:E,size:b,onPointerMissed:(...Se)=>Y.current==null?void 0:Y.current(...Se),onCreated:Se=>{Se.events.connect==null||Se.events.connect(c?Kb(c)?c.current:c:q.current),u&&Se.setEvents({compute:(Qe,Je)=>{const se=Qe[u+"X"],ge=Qe[u+"Y"];Je.pointer.set(se/Je.size.width*2-1,-(ge/Je.size.height)*2+1),Je.raycaster.setFromCamera(Je.pointer,Je.camera)}}),U==null||U(Se)}}),J.current.render(Ti.jsx(F,{children:Ti.jsx(Dy,{set:pe,children:Ti.jsx(ke.Suspense,{fallback:Ti.jsx(Qb,{set:le}),children:e??null})})})))}),ke.useEffect(()=>{const me=N.current;if(me)return()=>Hy(me)},[]);const xe=c?"none":"auto";return Ti.jsx("div",{ref:q,style:{position:"relative",width:"100%",height:"100%",overflow:"hidden",pointerEvents:xe,...i},...P,children:Ti.jsx("div",{ref:C,style:{width:"100%",height:"100%"},children:Ti.jsx("canvas",{ref:N,style:{display:"block"},children:t})})})}),XC=ke.forwardRef(function(e,t){return Ti.jsx(Xy,{children:Ti.jsx(PC,{...e,ref:t})})}),Yy=parseInt(Ja.replace(/\D+/g,"")),qy=Yy>=125?"uv1":"uv2";var IC=Object.defineProperty,LC=(r,e,t)=>e in r?IC(r,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):r[e]=t,DC=(r,e,t)=>(LC(r,e+"",t),t);class UC{constructor(){DC(this,"_listeners")}addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const n=this._listeners;n[e]===void 0&&(n[e]=[]),n[e].indexOf(t)===-1&&n[e].push(t)}hasEventListener(e,t){if(this._listeners===void 0)return!1;const n=this._listeners;return n[e]!==void 0&&n[e].indexOf(t)!==-1}removeEventListener(e,t){if(this._listeners===void 0)return;const i=this._listeners[e];if(i!==void 0){const s=i.indexOf(t);s!==-1&&i.splice(s,1)}}dispatchEvent(e){if(this._listeners===void 0)return;const n=this._listeners[e.type];if(n!==void 0){e.target=this;const i=n.slice(0);for(let s=0,l=i.length;s<l;s++)i[s].call(this,e);e.target=null}}}var NC=Object.defineProperty,OC=(r,e,t)=>e in r?NC(r,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):r[e]=t,ot=(r,e,t)=>(OC(r,typeof e!="symbol"?e+"":e,t),t);const nu=new Os,Mv=new hr,FC=Math.cos(70*(Math.PI/180)),Ev=(r,e)=>(r%e+e)%e;let BC=class extends UC{constructor(e,t){super(),ot(this,"object"),ot(this,"domElement"),ot(this,"enabled",!0),ot(this,"target",new L),ot(this,"minDistance",0),ot(this,"maxDistance",1/0),ot(this,"minZoom",0),ot(this,"maxZoom",1/0),ot(this,"minPolarAngle",0),ot(this,"maxPolarAngle",Math.PI),ot(this,"minAzimuthAngle",-1/0),ot(this,"maxAzimuthAngle",1/0),ot(this,"enableDamping",!1),ot(this,"dampingFactor",.05),ot(this,"enableZoom",!0),ot(this,"zoomSpeed",1),ot(this,"enableRotate",!0),ot(this,"rotateSpeed",1),ot(this,"enablePan",!0),ot(this,"panSpeed",1),ot(this,"screenSpacePanning",!0),ot(this,"keyPanSpeed",7),ot(this,"zoomToCursor",!1),ot(this,"autoRotate",!1),ot(this,"autoRotateSpeed",2),ot(this,"reverseOrbit",!1),ot(this,"reverseHorizontalOrbit",!1),ot(this,"reverseVerticalOrbit",!1),ot(this,"keys",{LEFT:"ArrowLeft",UP:"ArrowUp",RIGHT:"ArrowRight",BOTTOM:"ArrowDown"}),ot(this,"mouseButtons",{LEFT:gs.ROTATE,MIDDLE:gs.DOLLY,RIGHT:gs.PAN}),ot(this,"touches",{ONE:vs.ROTATE,TWO:vs.DOLLY_PAN}),ot(this,"target0"),ot(this,"position0"),ot(this,"zoom0"),ot(this,"_domElementKeyEvents",null),ot(this,"getPolarAngle"),ot(this,"getAzimuthalAngle"),ot(this,"setPolarAngle"),ot(this,"setAzimuthalAngle"),ot(this,"getDistance"),ot(this,"getZoomScale"),ot(this,"listenToKeyEvents"),ot(this,"stopListenToKeyEvents"),ot(this,"saveState"),ot(this,"reset"),ot(this,"update"),ot(this,"connect"),ot(this,"dispose"),ot(this,"dollyIn"),ot(this,"dollyOut"),ot(this,"getScale"),ot(this,"setScale"),this.object=e,this.domElement=t,this.target0=this.target.clone(),this.position0=this.object.position.clone(),this.zoom0=this.object.zoom,this.getPolarAngle=()=>f.phi,this.getAzimuthalAngle=()=>f.theta,this.setPolarAngle=H=>{let oe=Ev(H,2*Math.PI),Re=f.phi;Re<0&&(Re+=2*Math.PI),oe<0&&(oe+=2*Math.PI);let k=Math.abs(oe-Re);2*Math.PI-k<k&&(oe<Re?oe+=2*Math.PI:Re+=2*Math.PI),p.phi=oe-Re,n.update()},this.setAzimuthalAngle=H=>{let oe=Ev(H,2*Math.PI),Re=f.theta;Re<0&&(Re+=2*Math.PI),oe<0&&(oe+=2*Math.PI);let k=Math.abs(oe-Re);2*Math.PI-k<k&&(oe<Re?oe+=2*Math.PI:Re+=2*Math.PI),p.theta=oe-Re,n.update()},this.getDistance=()=>n.object.position.distanceTo(n.target),this.listenToKeyEvents=H=>{H.addEventListener("keydown",Ae),this._domElementKeyEvents=H},this.stopListenToKeyEvents=()=>{this._domElementKeyEvents.removeEventListener("keydown",Ae),this._domElementKeyEvents=null},this.saveState=()=>{n.target0.copy(n.target),n.position0.copy(n.object.position),n.zoom0=n.object.zoom},this.reset=()=>{n.target.copy(n.target0),n.object.position.copy(n.position0),n.object.zoom=n.zoom0,n.object.updateProjectionMatrix(),n.dispatchEvent(i),n.update(),u=c.NONE},this.update=(()=>{const H=new L,oe=new L(0,1,0),Re=new Un().setFromUnitVectors(e.up,oe),k=Re.clone().invert(),ye=new L,te=new Un,ue=2*Math.PI;return function(){const Ce=n.object.position;Re.setFromUnitVectors(e.up,oe),k.copy(Re).invert(),H.copy(Ce).sub(n.target),H.applyQuaternion(Re),f.setFromVector3(H),n.autoRotate&&u===c.NONE&&K(q()),n.enableDamping?(f.theta+=p.theta*n.dampingFactor,f.phi+=p.phi*n.dampingFactor):(f.theta+=p.theta,f.phi+=p.phi);let nt=n.minAzimuthAngle,It=n.maxAzimuthAngle;isFinite(nt)&&isFinite(It)&&(nt<-Math.PI?nt+=ue:nt>Math.PI&&(nt-=ue),It<-Math.PI?It+=ue:It>Math.PI&&(It-=ue),nt<=It?f.theta=Math.max(nt,Math.min(It,f.theta)):f.theta=f.theta>(nt+It)/2?Math.max(nt,f.theta):Math.min(It,f.theta)),f.phi=Math.max(n.minPolarAngle,Math.min(n.maxPolarAngle,f.phi)),f.makeSafe(),n.enableDamping===!0?n.target.addScaledVector(g,n.dampingFactor):n.target.add(g),n.zoomToCursor&&C||n.object.isOrthographicCamera?f.radius=Je(f.radius):f.radius=Je(f.radius*m),H.setFromSpherical(f),H.applyQuaternion(k),Ce.copy(n.target).add(H),n.object.matrixAutoUpdate||n.object.updateMatrix(),n.object.lookAt(n.target),n.enableDamping===!0?(p.theta*=1-n.dampingFactor,p.phi*=1-n.dampingFactor,g.multiplyScalar(1-n.dampingFactor)):(p.set(0,0,0),g.set(0,0,0));let Ht=!1;if(n.zoomToCursor&&C){let bt=null;if(n.object instanceof tn&&n.object.isPerspectiveCamera){const rn=H.length();bt=Je(rn*m);const Tn=rn-bt;n.object.position.addScaledVector(D,Tn),n.object.updateMatrixWorld()}else if(n.object.isOrthographicCamera){const rn=new L(F.x,F.y,0);rn.unproject(n.object),n.object.zoom=Math.max(n.minZoom,Math.min(n.maxZoom,n.object.zoom/m)),n.object.updateProjectionMatrix(),Ht=!0;const Tn=new L(F.x,F.y,0);Tn.unproject(n.object),n.object.position.sub(Tn).add(rn),n.object.updateMatrixWorld(),bt=H.length()}else console.warn("WARNING: OrbitControls.js encountered an unknown camera type - zoom to cursor disabled."),n.zoomToCursor=!1;bt!==null&&(n.screenSpacePanning?n.target.set(0,0,-1).transformDirection(n.object.matrix).multiplyScalar(bt).add(n.object.position):(nu.origin.copy(n.object.position),nu.direction.set(0,0,-1).transformDirection(n.object.matrix),Math.abs(n.object.up.dot(nu.direction))<FC?e.lookAt(n.target):(Mv.setFromNormalAndCoplanarPoint(n.object.up,n.target),nu.intersectPlane(Mv,n.target))))}else n.object instanceof kr&&n.object.isOrthographicCamera&&(Ht=m!==1,Ht&&(n.object.zoom=Math.max(n.minZoom,Math.min(n.maxZoom,n.object.zoom/m)),n.object.updateProjectionMatrix()));return m=1,C=!1,Ht||ye.distanceToSquared(n.object.position)>h||8*(1-te.dot(n.object.quaternion))>h?(n.dispatchEvent(i),ye.copy(n.object.position),te.copy(n.object.quaternion),Ht=!1,!0):!1}})(),this.connect=H=>{n.domElement=H,n.domElement.style.touchAction="none",n.domElement.addEventListener("contextmenu",_e),n.domElement.addEventListener("pointerdown",R),n.domElement.addEventListener("pointercancel",re),n.domElement.addEventListener("wheel",We)},this.dispose=()=>{var H,oe,Re,k,ye,te;n.domElement&&(n.domElement.style.touchAction="auto"),(H=n.domElement)==null||H.removeEventListener("contextmenu",_e),(oe=n.domElement)==null||oe.removeEventListener("pointerdown",R),(Re=n.domElement)==null||Re.removeEventListener("pointercancel",re),(k=n.domElement)==null||k.removeEventListener("wheel",We),(ye=n.domElement)==null||ye.ownerDocument.removeEventListener("pointermove",Z),(te=n.domElement)==null||te.ownerDocument.removeEventListener("pointerup",re),n._domElementKeyEvents!==null&&n._domElementKeyEvents.removeEventListener("keydown",Ae)};const n=this,i={type:"change"},s={type:"start"},l={type:"end"},c={NONE:-1,ROTATE:0,DOLLY:1,PAN:2,TOUCH_ROTATE:3,TOUCH_PAN:4,TOUCH_DOLLY_PAN:5,TOUCH_DOLLY_ROTATE:6};let u=c.NONE;const h=1e-6,f=new Qd,p=new Qd;let m=1;const g=new L,y=new ae,M=new ae,x=new ae,_=new ae,w=new ae,E=new ae,T=new ae,U=new ae,P=new ae,D=new L,F=new ae;let C=!1;const b=[],N={};function q(){return 2*Math.PI/60/60*n.autoRotateSpeed}function Y(){return Math.pow(.95,n.zoomSpeed)}function K(H){n.reverseOrbit||n.reverseHorizontalOrbit?p.theta+=H:p.theta-=H}function le(H){n.reverseOrbit||n.reverseVerticalOrbit?p.phi+=H:p.phi-=H}const $=(()=>{const H=new L;return function(Re,k){H.setFromMatrixColumn(k,0),H.multiplyScalar(-Re),g.add(H)}})(),pe=(()=>{const H=new L;return function(Re,k){n.screenSpacePanning===!0?H.setFromMatrixColumn(k,1):(H.setFromMatrixColumn(k,0),H.crossVectors(n.object.up,H)),H.multiplyScalar(Re),g.add(H)}})(),J=(()=>{const H=new L;return function(Re,k){const ye=n.domElement;if(ye&&n.object instanceof tn&&n.object.isPerspectiveCamera){const te=n.object.position;H.copy(te).sub(n.target);let ue=H.length();ue*=Math.tan(n.object.fov/2*Math.PI/180),$(2*Re*ue/ye.clientHeight,n.object.matrix),pe(2*k*ue/ye.clientHeight,n.object.matrix)}else ye&&n.object instanceof kr&&n.object.isOrthographicCamera?($(Re*(n.object.right-n.object.left)/n.object.zoom/ye.clientWidth,n.object.matrix),pe(k*(n.object.top-n.object.bottom)/n.object.zoom/ye.clientHeight,n.object.matrix)):(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - pan disabled."),n.enablePan=!1)}})();function xe(H){n.object instanceof tn&&n.object.isPerspectiveCamera||n.object instanceof kr&&n.object.isOrthographicCamera?m=H:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),n.enableZoom=!1)}function me(H){xe(m/H)}function Se(H){xe(m*H)}function Qe(H){if(!n.zoomToCursor||!n.domElement)return;C=!0;const oe=n.domElement.getBoundingClientRect(),Re=H.clientX-oe.left,k=H.clientY-oe.top,ye=oe.width,te=oe.height;F.x=Re/ye*2-1,F.y=-(k/te)*2+1,D.set(F.x,F.y,1).unproject(n.object).sub(n.object.position).normalize()}function Je(H){return Math.max(n.minDistance,Math.min(n.maxDistance,H))}function se(H){y.set(H.clientX,H.clientY)}function ge(H){Qe(H),T.set(H.clientX,H.clientY)}function Ve(H){_.set(H.clientX,H.clientY)}function we(H){M.set(H.clientX,H.clientY),x.subVectors(M,y).multiplyScalar(n.rotateSpeed);const oe=n.domElement;oe&&(K(2*Math.PI*x.x/oe.clientHeight),le(2*Math.PI*x.y/oe.clientHeight)),y.copy(M),n.update()}function et(H){U.set(H.clientX,H.clientY),P.subVectors(U,T),P.y>0?me(Y()):P.y<0&&Se(Y()),T.copy(U),n.update()}function lt(H){w.set(H.clientX,H.clientY),E.subVectors(w,_).multiplyScalar(n.panSpeed),J(E.x,E.y),_.copy(w),n.update()}function tt(H){Qe(H),H.deltaY<0?Se(Y()):H.deltaY>0&&me(Y()),n.update()}function ft(H){let oe=!1;switch(H.code){case n.keys.UP:J(0,n.keyPanSpeed),oe=!0;break;case n.keys.BOTTOM:J(0,-n.keyPanSpeed),oe=!0;break;case n.keys.LEFT:J(n.keyPanSpeed,0),oe=!0;break;case n.keys.RIGHT:J(-n.keyPanSpeed,0),oe=!0;break}oe&&(H.preventDefault(),n.update())}function he(){if(b.length==1)y.set(b[0].pageX,b[0].pageY);else{const H=.5*(b[0].pageX+b[1].pageX),oe=.5*(b[0].pageY+b[1].pageY);y.set(H,oe)}}function de(){if(b.length==1)_.set(b[0].pageX,b[0].pageY);else{const H=.5*(b[0].pageX+b[1].pageX),oe=.5*(b[0].pageY+b[1].pageY);_.set(H,oe)}}function z(){const H=b[0].pageX-b[1].pageX,oe=b[0].pageY-b[1].pageY,Re=Math.sqrt(H*H+oe*oe);T.set(0,Re)}function je(){n.enableZoom&&z(),n.enablePan&&de()}function ve(){n.enableZoom&&z(),n.enableRotate&&he()}function Oe(H){if(b.length==1)M.set(H.pageX,H.pageY);else{const Re=ze(H),k=.5*(H.pageX+Re.x),ye=.5*(H.pageY+Re.y);M.set(k,ye)}x.subVectors(M,y).multiplyScalar(n.rotateSpeed);const oe=n.domElement;oe&&(K(2*Math.PI*x.x/oe.clientHeight),le(2*Math.PI*x.y/oe.clientHeight)),y.copy(M)}function Te(H){if(b.length==1)w.set(H.pageX,H.pageY);else{const oe=ze(H),Re=.5*(H.pageX+oe.x),k=.5*(H.pageY+oe.y);w.set(Re,k)}E.subVectors(w,_).multiplyScalar(n.panSpeed),J(E.x,E.y),_.copy(w)}function it(H){const oe=ze(H),Re=H.pageX-oe.x,k=H.pageY-oe.y,ye=Math.sqrt(Re*Re+k*k);U.set(0,ye),P.set(0,Math.pow(U.y/T.y,n.zoomSpeed)),me(P.y),T.copy(U)}function Pe(H){n.enableZoom&&it(H),n.enablePan&&Te(H)}function O(H){n.enableZoom&&it(H),n.enableRotate&&Oe(H)}function R(H){var oe,Re;n.enabled!==!1&&(b.length===0&&((oe=n.domElement)==null||oe.ownerDocument.addEventListener("pointermove",Z),(Re=n.domElement)==null||Re.ownerDocument.addEventListener("pointerup",re)),He(H),H.pointerType==="touch"?Fe(H):fe(H))}function Z(H){n.enabled!==!1&&(H.pointerType==="touch"?St(H):ce(H))}function re(H){var oe,Re,k;rt(H),b.length===0&&((oe=n.domElement)==null||oe.releasePointerCapture(H.pointerId),(Re=n.domElement)==null||Re.ownerDocument.removeEventListener("pointermove",Z),(k=n.domElement)==null||k.ownerDocument.removeEventListener("pointerup",re)),n.dispatchEvent(l),u=c.NONE}function fe(H){let oe;switch(H.button){case 0:oe=n.mouseButtons.LEFT;break;case 1:oe=n.mouseButtons.MIDDLE;break;case 2:oe=n.mouseButtons.RIGHT;break;default:oe=-1}switch(oe){case gs.DOLLY:if(n.enableZoom===!1)return;ge(H),u=c.DOLLY;break;case gs.ROTATE:if(H.ctrlKey||H.metaKey||H.shiftKey){if(n.enablePan===!1)return;Ve(H),u=c.PAN}else{if(n.enableRotate===!1)return;se(H),u=c.ROTATE}break;case gs.PAN:if(H.ctrlKey||H.metaKey||H.shiftKey){if(n.enableRotate===!1)return;se(H),u=c.ROTATE}else{if(n.enablePan===!1)return;Ve(H),u=c.PAN}break;default:u=c.NONE}u!==c.NONE&&n.dispatchEvent(s)}function ce(H){if(n.enabled!==!1)switch(u){case c.ROTATE:if(n.enableRotate===!1)return;we(H);break;case c.DOLLY:if(n.enableZoom===!1)return;et(H);break;case c.PAN:if(n.enablePan===!1)return;lt(H);break}}function We(H){n.enabled===!1||n.enableZoom===!1||u!==c.NONE&&u!==c.ROTATE||(H.preventDefault(),n.dispatchEvent(s),tt(H),n.dispatchEvent(l))}function Ae(H){n.enabled===!1||n.enablePan===!1||ft(H)}function Fe(H){switch(ct(H),b.length){case 1:switch(n.touches.ONE){case vs.ROTATE:if(n.enableRotate===!1)return;he(),u=c.TOUCH_ROTATE;break;case vs.PAN:if(n.enablePan===!1)return;de(),u=c.TOUCH_PAN;break;default:u=c.NONE}break;case 2:switch(n.touches.TWO){case vs.DOLLY_PAN:if(n.enableZoom===!1&&n.enablePan===!1)return;je(),u=c.TOUCH_DOLLY_PAN;break;case vs.DOLLY_ROTATE:if(n.enableZoom===!1&&n.enableRotate===!1)return;ve(),u=c.TOUCH_DOLLY_ROTATE;break;default:u=c.NONE}break;default:u=c.NONE}u!==c.NONE&&n.dispatchEvent(s)}function St(H){switch(ct(H),u){case c.TOUCH_ROTATE:if(n.enableRotate===!1)return;Oe(H),n.update();break;case c.TOUCH_PAN:if(n.enablePan===!1)return;Te(H),n.update();break;case c.TOUCH_DOLLY_PAN:if(n.enableZoom===!1&&n.enablePan===!1)return;Pe(H),n.update();break;case c.TOUCH_DOLLY_ROTATE:if(n.enableZoom===!1&&n.enableRotate===!1)return;O(H),n.update();break;default:u=c.NONE}}function _e(H){n.enabled!==!1&&H.preventDefault()}function He(H){b.push(H)}function rt(H){delete N[H.pointerId];for(let oe=0;oe<b.length;oe++)if(b[oe].pointerId==H.pointerId){b.splice(oe,1);return}}function ct(H){let oe=N[H.pointerId];oe===void 0&&(oe=new ae,N[H.pointerId]=oe),oe.set(H.pageX,H.pageY)}function ze(H){const oe=H.pointerId===b[0].pointerId?b[1]:b[0];return N[oe.pointerId]}this.dollyIn=(H=Y())=>{Se(H),n.update()},this.dollyOut=(H=Y())=>{me(H),n.update()},this.getScale=()=>m,this.setScale=H=>{xe(H),n.update()},this.getZoomScale=()=>Y(),t!==void 0&&this.connect(t),this.update()}};const wv=new _n,iu=new L;class Zp extends zp{constructor(){super(),this.isLineSegmentsGeometry=!0,this.type="LineSegmentsGeometry";const e=[-1,2,0,1,2,0,-1,1,0,1,1,0,-1,0,0,1,0,0,-1,-1,0,1,-1,0],t=[-1,2,1,2,-1,1,1,1,-1,-1,1,-1,-1,-2,1,-2],n=[0,2,1,2,3,1,2,4,3,4,5,3,4,6,5,6,7,5];this.setIndex(n),this.setAttribute("position",new Ye(e,3)),this.setAttribute("uv",new Ye(t,2))}applyMatrix4(e){const t=this.attributes.instanceStart,n=this.attributes.instanceEnd;return t!==void 0&&(t.applyMatrix4(e),n.applyMatrix4(e),t.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}setPositions(e){let t;e instanceof Float32Array?t=e:Array.isArray(e)&&(t=new Float32Array(e));const n=new ju(t,6,1);return this.setAttribute("instanceStart",new si(n,3,0)),this.setAttribute("instanceEnd",new si(n,3,3)),this.computeBoundingBox(),this.computeBoundingSphere(),this}setColors(e,t=3){let n;e instanceof Float32Array?n=e:Array.isArray(e)&&(n=new Float32Array(e));const i=new ju(n,t*2,1);return this.setAttribute("instanceColorStart",new si(i,t,0)),this.setAttribute("instanceColorEnd",new si(i,t,t)),this}fromWireframeGeometry(e){return this.setPositions(e.attributes.position.array),this}fromEdgesGeometry(e){return this.setPositions(e.attributes.position.array),this}fromMesh(e){return this.fromWireframeGeometry(new Lp(e.geometry)),this}fromLineSegments(e){const t=e.geometry;return this.setPositions(t.attributes.position.array),this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new _n);const e=this.attributes.instanceStart,t=this.attributes.instanceEnd;e!==void 0&&t!==void 0&&(this.boundingBox.setFromBufferAttribute(e),wv.setFromBufferAttribute(t),this.boundingBox.union(wv))}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new yn),this.boundingBox===null&&this.computeBoundingBox();const e=this.attributes.instanceStart,t=this.attributes.instanceEnd;if(e!==void 0&&t!==void 0){const n=this.boundingSphere.center;this.boundingBox.getCenter(n);let i=0;for(let s=0,l=e.count;s<l;s++)iu.fromBufferAttribute(e,s),i=Math.max(i,n.distanceToSquared(iu)),iu.fromBufferAttribute(t,s),i=Math.max(i,n.distanceToSquared(iu));this.boundingSphere.radius=Math.sqrt(i),isNaN(this.boundingSphere.radius)&&console.error("THREE.LineSegmentsGeometry.computeBoundingSphere(): Computed radius is NaN. The instanced position data is likely to have NaN values.",this)}}toJSON(){}applyMatrix(e){return console.warn("THREE.LineSegmentsGeometry: applyMatrix() has been renamed to applyMatrix4()."),this.applyMatrix4(e)}}class Zy extends Zp{constructor(){super(),this.isLineGeometry=!0,this.type="LineGeometry"}setPositions(e){const t=e.length-3,n=new Float32Array(2*t);for(let i=0;i<t;i+=3)n[2*i]=e[i],n[2*i+1]=e[i+1],n[2*i+2]=e[i+2],n[2*i+3]=e[i+3],n[2*i+4]=e[i+4],n[2*i+5]=e[i+5];return super.setPositions(n),this}setColors(e,t=3){const n=e.length-t,i=new Float32Array(2*n);if(t===3)for(let s=0;s<n;s+=t)i[2*s]=e[s],i[2*s+1]=e[s+1],i[2*s+2]=e[s+2],i[2*s+3]=e[s+3],i[2*s+4]=e[s+4],i[2*s+5]=e[s+5];else for(let s=0;s<n;s+=t)i[2*s]=e[s],i[2*s+1]=e[s+1],i[2*s+2]=e[s+2],i[2*s+3]=e[s+3],i[2*s+4]=e[s+4],i[2*s+5]=e[s+5],i[2*s+6]=e[s+6],i[2*s+7]=e[s+7];return super.setColors(i,t),this}fromLine(e){const t=e.geometry;return this.setPositions(t.attributes.position.array),this}}class jp extends _i{constructor(e){super({type:"LineMaterial",uniforms:Xu.clone(Xu.merge([be.common,be.fog,{worldUnits:{value:1},linewidth:{value:1},resolution:{value:new ae(1,1)},dashOffset:{value:0},dashScale:{value:1},dashSize:{value:1},gapSize:{value:1}}])),vertexShader:`
				#include <common>
				#include <fog_pars_vertex>
				#include <logdepthbuf_pars_vertex>
				#include <clipping_planes_pars_vertex>

				uniform float linewidth;
				uniform vec2 resolution;

				attribute vec3 instanceStart;
				attribute vec3 instanceEnd;

				#ifdef USE_COLOR
					#ifdef USE_LINE_COLOR_ALPHA
						varying vec4 vLineColor;
						attribute vec4 instanceColorStart;
						attribute vec4 instanceColorEnd;
					#else
						varying vec3 vLineColor;
						attribute vec3 instanceColorStart;
						attribute vec3 instanceColorEnd;
					#endif
				#endif

				#ifdef WORLD_UNITS

					varying vec4 worldPos;
					varying vec3 worldStart;
					varying vec3 worldEnd;

					#ifdef USE_DASH

						varying vec2 vUv;

					#endif

				#else

					varying vec2 vUv;

				#endif

				#ifdef USE_DASH

					uniform float dashScale;
					attribute float instanceDistanceStart;
					attribute float instanceDistanceEnd;
					varying float vLineDistance;

				#endif

				void trimSegment( const in vec4 start, inout vec4 end ) {

					// trim end segment so it terminates between the camera plane and the near plane

					// conservative estimate of the near plane
					float a = projectionMatrix[ 2 ][ 2 ]; // 3nd entry in 3th column
					float b = projectionMatrix[ 3 ][ 2 ]; // 3nd entry in 4th column
					float nearEstimate = - 0.5 * b / a;

					float alpha = ( nearEstimate - start.z ) / ( end.z - start.z );

					end.xyz = mix( start.xyz, end.xyz, alpha );

				}

				void main() {

					#ifdef USE_COLOR

						vLineColor = ( position.y < 0.5 ) ? instanceColorStart : instanceColorEnd;

					#endif

					#ifdef USE_DASH

						vLineDistance = ( position.y < 0.5 ) ? dashScale * instanceDistanceStart : dashScale * instanceDistanceEnd;
						vUv = uv;

					#endif

					float aspect = resolution.x / resolution.y;

					// camera space
					vec4 start = modelViewMatrix * vec4( instanceStart, 1.0 );
					vec4 end = modelViewMatrix * vec4( instanceEnd, 1.0 );

					#ifdef WORLD_UNITS

						worldStart = start.xyz;
						worldEnd = end.xyz;

					#else

						vUv = uv;

					#endif

					// special case for perspective projection, and segments that terminate either in, or behind, the camera plane
					// clearly the gpu firmware has a way of addressing this issue when projecting into ndc space
					// but we need to perform ndc-space calculations in the shader, so we must address this issue directly
					// perhaps there is a more elegant solution -- WestLangley

					bool perspective = ( projectionMatrix[ 2 ][ 3 ] == - 1.0 ); // 4th entry in the 3rd column

					if ( perspective ) {

						if ( start.z < 0.0 && end.z >= 0.0 ) {

							trimSegment( start, end );

						} else if ( end.z < 0.0 && start.z >= 0.0 ) {

							trimSegment( end, start );

						}

					}

					// clip space
					vec4 clipStart = projectionMatrix * start;
					vec4 clipEnd = projectionMatrix * end;

					// ndc space
					vec3 ndcStart = clipStart.xyz / clipStart.w;
					vec3 ndcEnd = clipEnd.xyz / clipEnd.w;

					// direction
					vec2 dir = ndcEnd.xy - ndcStart.xy;

					// account for clip-space aspect ratio
					dir.x *= aspect;
					dir = normalize( dir );

					#ifdef WORLD_UNITS

						// get the offset direction as perpendicular to the view vector
						vec3 worldDir = normalize( end.xyz - start.xyz );
						vec3 offset;
						if ( position.y < 0.5 ) {

							offset = normalize( cross( start.xyz, worldDir ) );

						} else {

							offset = normalize( cross( end.xyz, worldDir ) );

						}

						// sign flip
						if ( position.x < 0.0 ) offset *= - 1.0;

						float forwardOffset = dot( worldDir, vec3( 0.0, 0.0, 1.0 ) );

						// don't extend the line if we're rendering dashes because we
						// won't be rendering the endcaps
						#ifndef USE_DASH

							// extend the line bounds to encompass  endcaps
							start.xyz += - worldDir * linewidth * 0.5;
							end.xyz += worldDir * linewidth * 0.5;

							// shift the position of the quad so it hugs the forward edge of the line
							offset.xy -= dir * forwardOffset;
							offset.z += 0.5;

						#endif

						// endcaps
						if ( position.y > 1.0 || position.y < 0.0 ) {

							offset.xy += dir * 2.0 * forwardOffset;

						}

						// adjust for linewidth
						offset *= linewidth * 0.5;

						// set the world position
						worldPos = ( position.y < 0.5 ) ? start : end;
						worldPos.xyz += offset;

						// project the worldpos
						vec4 clip = projectionMatrix * worldPos;

						// shift the depth of the projected points so the line
						// segments overlap neatly
						vec3 clipPose = ( position.y < 0.5 ) ? ndcStart : ndcEnd;
						clip.z = clipPose.z * clip.w;

					#else

						vec2 offset = vec2( dir.y, - dir.x );
						// undo aspect ratio adjustment
						dir.x /= aspect;
						offset.x /= aspect;

						// sign flip
						if ( position.x < 0.0 ) offset *= - 1.0;

						// endcaps
						if ( position.y < 0.0 ) {

							offset += - dir;

						} else if ( position.y > 1.0 ) {

							offset += dir;

						}

						// adjust for linewidth
						offset *= linewidth;

						// adjust for clip-space to screen-space conversion // maybe resolution should be based on viewport ...
						offset /= resolution.y;

						// select end
						vec4 clip = ( position.y < 0.5 ) ? clipStart : clipEnd;

						// back to clip space
						offset *= clip.w;

						clip.xy += offset;

					#endif

					gl_Position = clip;

					vec4 mvPosition = ( position.y < 0.5 ) ? start : end; // this is an approximation

					#include <logdepthbuf_vertex>
					#include <clipping_planes_vertex>
					#include <fog_vertex>

				}
			`,fragmentShader:`
				uniform vec3 diffuse;
				uniform float opacity;
				uniform float linewidth;

				#ifdef USE_DASH

					uniform float dashOffset;
					uniform float dashSize;
					uniform float gapSize;

				#endif

				varying float vLineDistance;

				#ifdef WORLD_UNITS

					varying vec4 worldPos;
					varying vec3 worldStart;
					varying vec3 worldEnd;

					#ifdef USE_DASH

						varying vec2 vUv;

					#endif

				#else

					varying vec2 vUv;

				#endif

				#include <common>
				#include <fog_pars_fragment>
				#include <logdepthbuf_pars_fragment>
				#include <clipping_planes_pars_fragment>

				#ifdef USE_COLOR
					#ifdef USE_LINE_COLOR_ALPHA
						varying vec4 vLineColor;
					#else
						varying vec3 vLineColor;
					#endif
				#endif

				vec2 closestLineToLine(vec3 p1, vec3 p2, vec3 p3, vec3 p4) {

					float mua;
					float mub;

					vec3 p13 = p1 - p3;
					vec3 p43 = p4 - p3;

					vec3 p21 = p2 - p1;

					float d1343 = dot( p13, p43 );
					float d4321 = dot( p43, p21 );
					float d1321 = dot( p13, p21 );
					float d4343 = dot( p43, p43 );
					float d2121 = dot( p21, p21 );

					float denom = d2121 * d4343 - d4321 * d4321;

					float numer = d1343 * d4321 - d1321 * d4343;

					mua = numer / denom;
					mua = clamp( mua, 0.0, 1.0 );
					mub = ( d1343 + d4321 * ( mua ) ) / d4343;
					mub = clamp( mub, 0.0, 1.0 );

					return vec2( mua, mub );

				}

				void main() {

					#include <clipping_planes_fragment>

					#ifdef USE_DASH

						if ( vUv.y < - 1.0 || vUv.y > 1.0 ) discard; // discard endcaps

						if ( mod( vLineDistance + dashOffset, dashSize + gapSize ) > dashSize ) discard; // todo - FIX

					#endif

					float alpha = opacity;

					#ifdef WORLD_UNITS

						// Find the closest points on the view ray and the line segment
						vec3 rayEnd = normalize( worldPos.xyz ) * 1e5;
						vec3 lineDir = worldEnd - worldStart;
						vec2 params = closestLineToLine( worldStart, worldEnd, vec3( 0.0, 0.0, 0.0 ), rayEnd );

						vec3 p1 = worldStart + lineDir * params.x;
						vec3 p2 = rayEnd * params.y;
						vec3 delta = p1 - p2;
						float len = length( delta );
						float norm = len / linewidth;

						#ifndef USE_DASH

							#ifdef USE_ALPHA_TO_COVERAGE

								float dnorm = fwidth( norm );
								alpha = 1.0 - smoothstep( 0.5 - dnorm, 0.5 + dnorm, norm );

							#else

								if ( norm > 0.5 ) {

									discard;

								}

							#endif

						#endif

					#else

						#ifdef USE_ALPHA_TO_COVERAGE

							// artifacts appear on some hardware if a derivative is taken within a conditional
							float a = vUv.x;
							float b = ( vUv.y > 0.0 ) ? vUv.y - 1.0 : vUv.y + 1.0;
							float len2 = a * a + b * b;
							float dlen = fwidth( len2 );

							if ( abs( vUv.y ) > 1.0 ) {

								alpha = 1.0 - smoothstep( 1.0 - dlen, 1.0 + dlen, len2 );

							}

						#else

							if ( abs( vUv.y ) > 1.0 ) {

								float a = vUv.x;
								float b = ( vUv.y > 0.0 ) ? vUv.y - 1.0 : vUv.y + 1.0;
								float len2 = a * a + b * b;

								if ( len2 > 1.0 ) discard;

							}

						#endif

					#endif

					vec4 diffuseColor = vec4( diffuse, alpha );
					#ifdef USE_COLOR
						#ifdef USE_LINE_COLOR_ALPHA
							diffuseColor *= vLineColor;
						#else
							diffuseColor.rgb *= vLineColor;
						#endif
					#endif

					#include <logdepthbuf_fragment>

					gl_FragColor = diffuseColor;

					#include <tonemapping_fragment>
					#include <${Yy>=154?"colorspace_fragment":"encodings_fragment"}>
					#include <fog_fragment>
					#include <premultiplied_alpha_fragment>

				}
			`,clipping:!0}),this.isLineMaterial=!0,this.onBeforeCompile=function(){this.transparent?this.defines.USE_LINE_COLOR_ALPHA="1":delete this.defines.USE_LINE_COLOR_ALPHA},Object.defineProperties(this,{color:{enumerable:!0,get:function(){return this.uniforms.diffuse.value},set:function(t){this.uniforms.diffuse.value=t}},worldUnits:{enumerable:!0,get:function(){return"WORLD_UNITS"in this.defines},set:function(t){t===!0?this.defines.WORLD_UNITS="":delete this.defines.WORLD_UNITS}},linewidth:{enumerable:!0,get:function(){return this.uniforms.linewidth.value},set:function(t){this.uniforms.linewidth.value=t}},dashed:{enumerable:!0,get:function(){return"USE_DASH"in this.defines},set(t){!!t!="USE_DASH"in this.defines&&(this.needsUpdate=!0),t===!0?this.defines.USE_DASH="":delete this.defines.USE_DASH}},dashScale:{enumerable:!0,get:function(){return this.uniforms.dashScale.value},set:function(t){this.uniforms.dashScale.value=t}},dashSize:{enumerable:!0,get:function(){return this.uniforms.dashSize.value},set:function(t){this.uniforms.dashSize.value=t}},dashOffset:{enumerable:!0,get:function(){return this.uniforms.dashOffset.value},set:function(t){this.uniforms.dashOffset.value=t}},gapSize:{enumerable:!0,get:function(){return this.uniforms.gapSize.value},set:function(t){this.uniforms.gapSize.value=t}},opacity:{enumerable:!0,get:function(){return this.uniforms.opacity.value},set:function(t){this.uniforms.opacity.value=t}},resolution:{enumerable:!0,get:function(){return this.uniforms.resolution.value},set:function(t){this.uniforms.resolution.value.copy(t)}},alphaToCoverage:{enumerable:!0,get:function(){return"USE_ALPHA_TO_COVERAGE"in this.defines},set:function(t){!!t!="USE_ALPHA_TO_COVERAGE"in this.defines&&(this.needsUpdate=!0),t===!0?(this.defines.USE_ALPHA_TO_COVERAGE="",this.extensions.derivatives=!0):(delete this.defines.USE_ALPHA_TO_COVERAGE,this.extensions.derivatives=!1)}}}),this.setValues(e)}}const Id=new At,Tv=new L,Av=new L,Sn=new At,Mn=new At,Hi=new At,Ld=new L,Dd=new ut,En=new Ay,bv=new L,ru=new _n,su=new yn,Vi=new At;let Wi,Ps;function Cv(r,e,t){return Vi.set(0,0,-e,1).applyMatrix4(r.projectionMatrix),Vi.multiplyScalar(1/Vi.w),Vi.x=Ps/t.width,Vi.y=Ps/t.height,Vi.applyMatrix4(r.projectionMatrixInverse),Vi.multiplyScalar(1/Vi.w),Math.abs(Math.max(Vi.x,Vi.y))}function zC(r,e){const t=r.matrixWorld,n=r.geometry,i=n.attributes.instanceStart,s=n.attributes.instanceEnd,l=Math.min(n.instanceCount,i.count);for(let c=0,u=l;c<u;c++){En.start.fromBufferAttribute(i,c),En.end.fromBufferAttribute(s,c),En.applyMatrix4(t);const h=new L,f=new L;Wi.distanceSqToSegment(En.start,En.end,f,h),f.distanceTo(h)<Ps*.5&&e.push({point:f,pointOnLine:h,distance:Wi.origin.distanceTo(f),object:r,face:null,faceIndex:c,uv:null,[qy]:null})}}function kC(r,e,t){const n=e.projectionMatrix,s=r.material.resolution,l=r.matrixWorld,c=r.geometry,u=c.attributes.instanceStart,h=c.attributes.instanceEnd,f=Math.min(c.instanceCount,u.count),p=-e.near;Wi.at(1,Hi),Hi.w=1,Hi.applyMatrix4(e.matrixWorldInverse),Hi.applyMatrix4(n),Hi.multiplyScalar(1/Hi.w),Hi.x*=s.x/2,Hi.y*=s.y/2,Hi.z=0,Ld.copy(Hi),Dd.multiplyMatrices(e.matrixWorldInverse,l);for(let m=0,g=f;m<g;m++){if(Sn.fromBufferAttribute(u,m),Mn.fromBufferAttribute(h,m),Sn.w=1,Mn.w=1,Sn.applyMatrix4(Dd),Mn.applyMatrix4(Dd),Sn.z>p&&Mn.z>p)continue;if(Sn.z>p){const E=Sn.z-Mn.z,T=(Sn.z-p)/E;Sn.lerp(Mn,T)}else if(Mn.z>p){const E=Mn.z-Sn.z,T=(Mn.z-p)/E;Mn.lerp(Sn,T)}Sn.applyMatrix4(n),Mn.applyMatrix4(n),Sn.multiplyScalar(1/Sn.w),Mn.multiplyScalar(1/Mn.w),Sn.x*=s.x/2,Sn.y*=s.y/2,Mn.x*=s.x/2,Mn.y*=s.y/2,En.start.copy(Sn),En.start.z=0,En.end.copy(Mn),En.end.z=0;const M=En.closestPointToPointParameter(Ld,!0);En.at(M,bv);const x=__.lerp(Sn.z,Mn.z,M),_=x>=-1&&x<=1,w=Ld.distanceTo(bv)<Ps*.5;if(_&&w){En.start.fromBufferAttribute(u,m),En.end.fromBufferAttribute(h,m),En.start.applyMatrix4(l),En.end.applyMatrix4(l);const E=new L,T=new L;Wi.distanceSqToSegment(En.start,En.end,T,E),t.push({point:T,pointOnLine:E,distance:Wi.origin.distanceTo(T),object:r,face:null,faceIndex:m,uv:null,[qy]:null})}}}class jy extends nn{constructor(e=new Zp,t=new jp({color:Math.random()*16777215})){super(e,t),this.isLineSegments2=!0,this.type="LineSegments2"}computeLineDistances(){const e=this.geometry,t=e.attributes.instanceStart,n=e.attributes.instanceEnd,i=new Float32Array(2*t.count);for(let l=0,c=0,u=t.count;l<u;l++,c+=2)Tv.fromBufferAttribute(t,l),Av.fromBufferAttribute(n,l),i[c]=c===0?0:i[c-1],i[c+1]=i[c]+Tv.distanceTo(Av);const s=new ju(i,2,1);return e.setAttribute("instanceDistanceStart",new si(s,1,0)),e.setAttribute("instanceDistanceEnd",new si(s,1,1)),this}raycast(e,t){const n=this.material.worldUnits,i=e.camera;i===null&&!n&&console.error('LineSegments2: "Raycaster.camera" needs to be set in order to raycast against LineSegments2 while worldUnits is set to false.');const s=e.params.Line2!==void 0&&e.params.Line2.threshold||0;Wi=e.ray;const l=this.matrixWorld,c=this.geometry,u=this.material;Ps=u.linewidth+s,c.boundingSphere===null&&c.computeBoundingSphere(),su.copy(c.boundingSphere).applyMatrix4(l);let h;if(n)h=Ps*.5;else{const p=Math.max(i.near,su.distanceToPoint(Wi.origin));h=Cv(i,p,u.resolution)}if(su.radius+=h,Wi.intersectsSphere(su)===!1)return;c.boundingBox===null&&c.computeBoundingBox(),ru.copy(c.boundingBox).applyMatrix4(l);let f;if(n)f=Ps*.5;else{const p=Math.max(i.near,ru.distanceToPoint(Wi.origin));f=Cv(i,p,u.resolution)}ru.expandByScalar(f),Wi.intersectsBox(ru)!==!1&&(n?zC(this,t):kC(this,i,t))}onBeforeRender(e){const t=this.material.uniforms;t&&t.resolution&&(e.getViewport(Id),this.material.uniforms.resolution.value.set(Id.z,Id.w))}}class HC extends jy{constructor(e=new Zy,t=new jp({color:Math.random()*16777215})){super(e,t),this.isLine2=!0,this.type="Line2"}}const qC=ke.forwardRef(function({points:e,color:t=16777215,vertexColors:n,linewidth:i,lineWidth:s,segments:l,dashed:c,...u},h){var f,p;const m=ur(_=>_.size),g=ke.useMemo(()=>l?new jy:new HC,[l]),[y]=ke.useState(()=>new jp),M=(n==null||(f=n[0])==null?void 0:f.length)===4?4:3,x=ke.useMemo(()=>{const _=l?new Zp:new Zy,w=e.map(E=>{const T=Array.isArray(E);return E instanceof L||E instanceof At?[E.x,E.y,E.z]:E instanceof ae?[E.x,E.y,0]:T&&E.length===3?[E[0],E[1],E[2]]:T&&E.length===2?[E[0],E[1],0]:E});if(_.setPositions(w.flat()),n){t=16777215;const E=n.map(T=>T instanceof Be?T.toArray():T);_.setColors(E.flat(),M)}return _},[e,l,n,M]);return ke.useLayoutEffect(()=>{g.computeLineDistances()},[e,g]),ke.useLayoutEffect(()=>{c?y.defines.USE_DASH="":delete y.defines.USE_DASH,y.needsUpdate=!0},[c,y]),ke.useEffect(()=>()=>{x.dispose(),y.dispose()},[x]),ke.createElement("primitive",Nd({object:g,ref:h},u),ke.createElement("primitive",{object:x,attach:"geometry"}),ke.createElement("primitive",Nd({object:y,attach:"material",color:t,vertexColors:!!n,resolution:[m.width,m.height],linewidth:(p=i??s)!==null&&p!==void 0?p:1,dashed:c,transparent:M===4},u)))}),ZC=ke.forwardRef(({makeDefault:r,camera:e,regress:t,domElement:n,enableDamping:i=!0,keyEvents:s=!1,onChange:l,onStart:c,onEnd:u,...h},f)=>{const p=ur(P=>P.invalidate),m=ur(P=>P.camera),g=ur(P=>P.gl),y=ur(P=>P.events),M=ur(P=>P.setEvents),x=ur(P=>P.set),_=ur(P=>P.get),w=ur(P=>P.performance),E=e||m,T=n||y.connected||g.domElement,U=ke.useMemo(()=>new BC(E),[E]);return uC(()=>{U.enabled&&U.update()},-1),ke.useEffect(()=>(s&&U.connect(s===!0?T:s),U.connect(T),()=>void U.dispose()),[s,T,t,U,p]),ke.useEffect(()=>{const P=C=>{p(),t&&w.regress(),l&&l(C)},D=C=>{c&&c(C)},F=C=>{u&&u(C)};return U.addEventListener("change",P),U.addEventListener("start",D),U.addEventListener("end",F),()=>{U.removeEventListener("start",D),U.removeEventListener("end",F),U.removeEventListener("change",P)}},[l,c,u,U,p,M]),ke.useEffect(()=>{if(r){const P=_().controls;return x({controls:U}),()=>x({controls:P})}},[r,U]),ke.createElement("primitive",Nd({ref:f,object:U,enableDamping:i},h))});export{Fd as A,_n as B,Be as C,Gi as D,qC as L,ut as M,ZC as O,vs as T,L as V,uC as a,xt as b,zt as c,Vr as d,Gn as e,ae as f,__ as g,XC as h,uA as i,ur as u};
