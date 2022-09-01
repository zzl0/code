// https://algs4.cs.princeton.edu/53substring/KMP.java.html

pub struct KMP {
    m: usize,
    dfa: Vec<Vec<usize>>,
}

impl KMP {
    pub fn new(pat: String) -> KMP {
        let r = 256;
        let pat = pat.into_bytes();
        let m = pat.len();

        // build DFA from pattern
        let mut dfa = vec![vec![0; m]; r];
        dfa[pat[0] as usize][0] = 1;
        let mut x = 0;
        for j in 1..m {
            for c in 0..r {
                dfa[c][j] = dfa[c][x];
            }
            dfa[pat[j] as usize][j] = j + 1;
            x = dfa[pat[j] as usize][x];
        }
        KMP {m, dfa}
    }

    pub fn search(&self, txt: String) -> usize {
        let txt = txt.into_bytes();
        let n = txt.len();
        let mut i = 0;
        let mut j = 0;
        while i < n && j < self.m {
            j = self.dfa[txt[i] as usize][j];
            i += 1;
        }
        if j == self.m {
            return i - self.m;
        }
        n
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_match() {
        let kmp = KMP::new("abra".to_string());
        assert_eq!(6, kmp.search("abacadabrac".to_string()));
        assert_eq!(1, kmp.search("cabra".to_string()));
    }

    #[test]
    fn test_mismatch() {
        let kmp = KMP::new("abra".to_string());
        assert_eq!(5, kmp.search("cabre".to_string()));
    }
}
