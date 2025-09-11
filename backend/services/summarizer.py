# services/summarizer.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class ResultSummarizer:
    """Generates AI-powered summaries from analysis results using Gemini"""

    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCE4Bzqf_cHDKN33JNbhV98tGNbsNN-w78')
        genai.configure(api_key=api_key)

        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Fallback to rule-based if AI fails
        self.fallback_summarizer = self._create_fallback_summarizer()

    def generate_summary(self, analysis_results):
        """
        Generate AI-powered summary from analysis results
        """
        # =================================================================
        # 🔍 DEBUG: Show complete input data structure
        # =================================================================
        print("\n" + "="*80)
        print("🔍 SUMMARIZER DEBUG - COMPLETE INPUT ANALYSIS")
        print("="*80)
        
        print(f"📊 Input Data Type: {type(analysis_results)}")
        print(f"📋 Input Data Keys: {list(analysis_results.keys()) if isinstance(analysis_results, dict) else 'Not a dict'}")
        
        print(f"\n📄 COMPLETE RAW INPUT DATA:")
        print("-" * 60)
        import json
        try:
            formatted_input = json.dumps(analysis_results, indent=2, default=str)
            print(formatted_input)
        except Exception as e:
            print(f"Could not JSON format input: {e}")
            print(f"Raw input: {analysis_results}")
        print("-" * 60)
        
        # Show specific sections if they exist
        if isinstance(analysis_results, dict):
            if "analyses" in analysis_results:
                print(f"\n🔬 ANALYSES SECTION:")
                analyses = analysis_results["analyses"]
                print(f"   Type: {type(analyses)}")
                print(f"   Keys: {list(analyses.keys()) if isinstance(analyses, dict) else 'Not a dict'}")
                if isinstance(analyses, dict):
                    for key, value in analyses.items():
                        print(f"   📌 {key}: {type(value)} - {str(value)[:100]}...")
            
            if "overall_assessment" in analysis_results:
                print(f"\n🎯 OVERALL ASSESSMENT:")
                overall = analysis_results["overall_assessment"]
                print(f"   Type: {type(overall)}")
                print(f"   Content: {overall}")
        
        print("="*80)
        # =================================================================
        
        try:
            # Check if analysis failed
            if analysis_results.get("status") == "error":
                print("❌ Analysis status indicates error")
                return {
                    "summary": f"Analysis failed: {analysis_results.get('error', 'Unknown error')}",
                    "score": 0,
                    "recommendation": "Unable to analyze image"
                }

            print("🚀 Proceeding with AI summary generation...")
            
            # Generate AI summary using Gemini
            ai_summary = self._generate_ai_summary(analysis_results)
            print(f"✅ AI Summary generated: {len(ai_summary)} characters")

            # Extract key metrics for structured response
            analyses = analysis_results.get("analyses", {})
            overall = analysis_results.get("overall_assessment", {})

            confidence = overall.get("confidence_score", 0) * 100
            is_deepfake = overall.get("is_likely_deepfake", False)
            
            print(f"📊 Extracted metrics:")
            print(f"   Confidence: {confidence}%")
            print(f"   Is Deepfake: {is_deepfake}")

            result = {
                "summary": ai_summary,
                "score": int(confidence),
                "is_deepfake": is_deepfake,
                "recommendation": overall.get('recommendation', 'Analysis completed'),
                "technical_details": self._extract_technical_details(analyses)
            }
            
            print(f"\n🎉 FINAL SUMMARY RESULT:")
            print(f"   Summary length: {len(result['summary'])} chars")
            print(f"   Score: {result['score']}%")
            print(f"   Is Deepfake: {result['is_deepfake']}")
            print(f"   Recommendation: {result['recommendation']}")
            print("="*80 + "\n")
            
            return result

        except Exception as e:
            print(f"❌ AI summarization failed: {e}. Using fallback.")
            print(f"🔄 Falling back to rule-based summarizer...")
            return self.fallback_summarizer.generate_summary(analysis_results)

    def _generate_ai_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Use Gemini to generate a natural language summary of the analysis results
        """
        print(f"\n🤖 GENERATING AI SUMMARY:")
        
        # Prepare the analysis data as context for Gemini
        context = self._prepare_analysis_context(analysis_results)

        # Create the prompt for Gemini
        prompt = f"""
        You are an expert deepfake detection analyst. Based on the following analysis results,
        provide a comprehensive summary in 2-3 paragraphs that explains:

        1. The overall authenticity assessment
        2. Key findings from each analysis type
        3. Confidence level and recommendation
        4. Any suspicious indicators found

        Analysis Results:
        {context}

        Please provide a clear, professional summary that would be understandable to both technical and non-technical users.
        """

        print(f"   📝 Prompt length: {len(prompt)} characters")
        print(f"   🎯 Calling Gemini API...")

        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            ai_response = response.text.strip()
            
            print(f"   ✅ Gemini response received!")
            print(f"   📏 Response length: {len(ai_response)} characters")
            print(f"   📄 Response preview: {ai_response[:150]}...")
            
            return ai_response

        except Exception as e:
            print(f"   ❌ Gemini API error: {e}")
            raise e

    def _prepare_analysis_context(self, results: Dict[str, Any]) -> str:
        """
        Convert analysis results into a structured text format for Gemini
        """
        print(f"\n🔧 PREPARING GEMINI CONTEXT:")
        print(f"   Input type: {type(results)}")
        
        context_parts = []

        # Overall assessment
        overall = results.get("overall_assessment", {})
        confidence = overall.get("confidence_score", 0) * 100
        is_deepfake = overall.get("is_likely_deepfake", False)

        print(f"   📊 Overall Assessment found: {bool(overall)}")
        print(f"   📈 Confidence: {confidence}%")
        print(f"   🎯 Is Deepfake: {is_deepfake}")

        context_parts.append(f"OVERALL ASSESSMENT:")
        context_parts.append(f"- Authenticity Confidence: {confidence:.1f}%")
        context_parts.append(f"- Classification: {'Likely Deepfake' if is_deepfake else 'Likely Authentic'}")
        context_parts.append(f"- Recommendation: {overall.get('recommendation', 'No recommendation')}")
        context_parts.append("")

        # Individual analysis results
        analyses = results.get("analyses", {})
        print(f"   🔬 Analyses found: {len(analyses) if analyses else 0} items")
        
        context_parts.append("DETAILED ANALYSIS RESULTS:")

        for analysis_name, analysis_data in analyses.items():
            operation = analysis_data.get("operation", analysis_name.replace("_", " ").title())
            flag = analysis_data.get("flag", "Unknown")
            description = analysis_data.get("description", "No description available")

            print(f"     📌 {analysis_name}: {flag} - {operation}")

            # Extract score if available
            score_info = ""
            if "result" in analysis_data and isinstance(analysis_data["result"], dict):
                if "suspicious_score" in analysis_data["result"]:
                    score = analysis_data["result"]["suspicious_score"]
                    score_info = f" (Suspicious Score: {score})"
                    print(f"       🔢 Suspicious Score: {score}")

            context_parts.append(f"- {operation}: {description}{score_info} [{flag}]")

        final_context = "\n".join(context_parts)
        print(f"   📝 Generated context: {len(final_context)} characters")
        print(f"   📄 Context preview: {final_context[:200]}...")
        
        return final_context

    def _extract_technical_details(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract technical details for frontend display
        """
        technical_details = {}

        for analysis_name, analysis_data in analyses.items():
            technical_details[analysis_name] = {
                "operation": analysis_data.get("operation", analysis_name.replace("_", " ").title()),
                "flag": analysis_data.get("flag", "Unknown"),
                "description": analysis_data.get("description", "No description available")
            }

        return technical_details

    def _create_fallback_summarizer(self):
        """
        Fallback to the original rule-based summarizer if AI fails
        """
        class FallbackSummarizer:
            def generate_summary(self, analysis_results):
                # Original rule-based logic
                if analysis_results.get("status") == "error":
                    return {
                        "summary": f"Analysis failed: {analysis_results.get('error', 'Unknown error')}",
                        "score": 0,
                        "recommendation": "Unable to analyze image"
                    }

                analyses = analysis_results.get("analyses", {})
                overall = analysis_results.get("overall_assessment", {})

                # Build summary sections
                summary_sections = []
                summary_sections.append("=== DEEPFAKE DETECTION ANALYSIS REPORT ===\n")

                # Overall assessment
                confidence = overall.get("confidence_score", 0) * 100
                is_deepfake = overall.get("is_likely_deepfake", False)

                summary_sections.append("OVERALL ASSESSMENT:")
                summary_sections.append(f"• Authenticity Confidence: {confidence:.1f}%")
                summary_sections.append(f"• Classification: {'LIKELY DEEPFAKE' if is_deepfake else 'LIKELY AUTHENTIC'}")
                summary_sections.append(f"• Recommendation: {overall.get('recommendation', 'No recommendation available')}")
                summary_sections.append("")

                # Detailed analysis results
                summary_sections.append("DETAILED ANALYSIS RESULTS:")

                for analysis_name, analysis_data in analyses.items():
                    operation = analysis_data.get("operation", analysis_name.replace("_", " ").title())
                    flag = analysis_data.get("flag", "Unknown")
                    description = analysis_data.get("description", "No description available")

                    status_emoji = "❌" if flag == "Suspicious" else "✅" if flag == "Passed" else "⚠️"
                    summary_sections.append(f"{status_emoji} {operation}: {description}")

                summary_sections.append("")
                summary_sections.append("=== END REPORT ===")

                return {
                    "summary": "\n".join(summary_sections),
                    "score": int(confidence),
                    "is_deepfake": is_deepfake,
                    "recommendation": overall.get('recommendation', 'Analysis completed'),
                    "technical_details": {}
                }

        return FallbackSummarizer()


def summarize_results(results: list):
    """
    Legacy function - creates a human-readable summary from JSON results.
    Also computes an overall authenticity score.
    """

    summary_lines = []
    score = 100  # start with 100% authenticity

    for i, res in enumerate(results, start=1):
        summary_lines.append(f"{i}. {res['operation']}: {res['description']}")

        # Adjust score based on flags
        if res["flag"] == "Anomaly" or res["flag"] == "Suspicious":
            score -= 15
        elif res["flag"] == "Error":
            score -= 10

    # Clamp score between 0 and 100
    score = max(0, min(100, score))
    summary_lines.append(f"Overall authenticity score: {score}%")

    return "\n".join(summary_lines), score
 