export type LearningStatus = 'unassessed' | 'learning' | 'explainable' | 'understood';
export type VerificationStatus = 'proposed' | 'investigating' | 'verified' | 'rejected';
export interface Concept {
  id: string; name: string; aliases: string[]; type: string; domain: string; description: string;
  formula?: string | null; tags: string[]; sourceIds: string[];
  learningStatus: LearningStatus; questions: string[];
}
export interface Relation {
  id: string; source: string; target: string; type: string; directed: boolean;
  description: string; conditions: string; evidence: string; sourceIds: string[];
  verificationStatus: VerificationStatus; provenance: string; questions: string[];
  limitations: string; sourceLocator: string; reviewNote?: string;
}
export interface Source { id: string; title: string; kind: string; path?: string; url?: string; locator: string }
export interface Content { id: string; title: string; path: string; conceptIds: string[]; status: string; note: string }
export interface Atlas { concepts: Concept[]; relations: Relation[]; sources: Source[]; contents: Content[] }
export const learningLabels: Record<LearningStatus, string> = {unassessed:'아직 평가하지 않음', learning:'학습 중', explainable:'예제로 설명 가능', understood:'조건·한계까지 설명 가능'};
export const verificationLabels: Record<VerificationStatus, string> = {proposed:'탐구 후보', investigating:'조사 중', verified:'근거 확인', rejected:'기각'};
export const relationLabels: Record<string,string> = {prerequisite:'선행 개념', generalization:'일반화', specialization:'특수화', equivalence:'동치', isomorphism:'동형', representation:'표현', transformation:'변환', application:'응용', derivation:'유도', shared_strategy:'공통 전략', analogy:'직관적 유사성', related_to:'관련성'};
export const colors: Record<string,string> = {'해석학':'#a69cfa','선형대수':'#65c9c1','물리학':'#edb96e','통계학':'#df94b6','공통 아이디어':'#91a8c3'};
