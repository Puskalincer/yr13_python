import { CountUp } from '../js/countUp.min.js';




var score = [];

export function generate_score_ob(player_number){
    for (let i = 0; i < player_number; i++) {

        if(!score[i]){
            score[i] = 0
        }
        
        score[i] = new CountUp('score_'+i, 0);
        score[i].start()
    }
}


export function update_score_ob(score_array){
    for (let i = 0; i < score.length; i++) {
        score[i].update(score_array[i]);
    }
}