<template>
    <div id="t" class="container">
        {{give}}
        <div v-for="value,index in question_list">
            <div v-if="Object.prototype.toString.call(value).slice(8,-1)=='Array'">
                <div v-for="x,y in value">
                    <div v-if="y==0">
                        <span>{{x}}</span><br>
                        <div v-if="Object.prototype.toString.call(answer_list[index]).slice(8,-1)=='Array'">
                            <select  :id="question_id[index][y]" @change="change(index)">
                                <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                            </select>
                        </div>
                    </div>
                    <div v-if="y!=0&&is_show[index]">
                        <span  v-if="x.slice(-1,x.length+1)=='+'">{{x.slice(0,-1)}}(可复选)</span>
                        <span  v-else="x.slice(-1,x.length+1)=='+'">{{x}}</span><br>
                        <div v-if="Object.prototype.toString.call(answer_list[index][y]).slice(8,-1)=='Array'">
                            <div v-if="x.slice(-1,x.length+1)=='+'">
                                <select multiple="ture" :id="question_id[index][y]">
                                    <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                                </select>
                            </div>
                            <div v-else="x.slice(-1,x.length+1)=='+'">
                                <select  :id="question_id[index][y]">
                                    <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                                </select>
                            </div>
                        </div>
                        <div v-else="Object.prototype.toString.call(answer_list[index][y]).slice(8,-1)=='Array'">
                            <input type="text"  :id="question_id[index][y]">
                        </div>
                    </div>
                </div>
            </div>
            <div v-else="Object.prototype.toString.call(value).slice(8,-1)=='Array'">
                
                <span  v-if="value.slice(-1,value.length+1)=='+'">{{value.slice(0,-1)}}(可复选)</span>
                <span  v-else="value.slice(-1,value.length+1)=='+'">{{value}}</span><br>
                <input v-if="answer_list[index]==''" type="text"  :id="question_id[index]">
                <div v-if="Object.prototype.toString.call(answer_list[index]).slice(8,-1)=='Array'">
                    <div v-if="value.slice(-1,value.length+1)=='+'">
                        <select multiple="ture" :id="question_id[index]">
                            <option v-for="part in answer_list[index]" :value="part">{{part}}</option>
                        </select>
                    </div>
                    <div v-else="value.slice(-1,value.length+1)=='+'">
                        <select  :id="question_id[index]">
                            <option v-for="part in answer_list[index]" :value="part">{{part}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return{
            question_list:[['您有做例行健康检查或病情追踪的习惯吗？', '若是有，多久检查一次：', '最近一次检查时间：', '通常您做检查的医院是：+', '科别：'],
                            '姓名','年龄','爱好：+',
                            ['您有做例行健康检查或病情追踪的习惯吗？', '若是有，多久检查一次：', '最近一次检查时间：', '通常您做检查的医院是：+', '科别：']],
            question_id:[['a','b','c','d','e'],'f','g','h',['aa','bb','cc','dd','ee']],
            answer_list:[[['有', '无'], '', [1,2],['a','b','c'] ,''],'','',['q','w','e','r'],[['有', '无'], '', [1,2],['a','b','c'] ,'']],
            solve_question_answer:[['有', 'aa', 2, ['a','c'], 'w'],'师玲珑',14,['q','r'],['有', 'qq', 1, ['a','b'], 'ww']],
            is_show:{'0':true,'4':true}
        }
    },
    computed:{
        give:function(){
            this.timer = setTimeout(()=>{   
                this.give_answer()  
            },100);
        },
        
    },
    methods:{
        change:function(index){
            if(document.getElementById(this.question_id[index][0]).value=='有'){
                this.is_show[index]=true
            }else{
                this.is_show[index]=false
                for(var i=1;i<this.question_id[index].length;i++){
                    document.getElementById(this.question_id[index][i]).value=''
                }
            }
        },
        give_answer:function(){
            for(var x=0;x<this.question_id.length;x++){
                if(typeof(this.question_id[x])=='object'){
                    for(var y=0;y<this.question_id[x].length;y++){
                        if(document.getElementById(this.question_id[x][y])){
                            if(typeof(this.solve_question_answer[x][y])=='object'){
                                const options=document.getElementById(this.question_id[x][y]).options
                                for(var q=0;q<options.length;q++){
                                    for(var z=0;z<this.solve_question_answer[x][y].length;z++){
                                        if(options[q].value==this.solve_question_answer[x][y][z]){
                                            options[q].selected=true
                                        }
                                    }
                                }
                            }else{
                                document.getElementById(this.question_id[x][y]).value=this.solve_question_answer[x][y]
                            }
                        }
                        this.change(x)
                    }
                }else{
                    if(typeof(this.solve_question_answer[x])=='object'){
                        const options=document.getElementById(this.question_id[x]).options
                        for(var y=0;y<options.length;y++){
                            for(var xx=0;xx<this.solve_question_answer[x].length;xx++){
                                if(options[y].value==this.solve_question_answer[x][xx]){
                                    options[y].selected=true
                                }
                            }
                        }
                        
                    }else{
                        document.getElementById(this.question_id[x]).value=this.solve_question_answer[x]
                    }
                }
            }
            
        }
    }
}
</script>