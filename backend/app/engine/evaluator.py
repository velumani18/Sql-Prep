import time
from typing import List
from app.engine.db_manager import db_manager
from app.engine.types import (
    ExecutionMode,
    QueryResult,
    SubmissionResult,
    TestCaseEvaluation,
)
from app.engine.validator import evaluate_query_results
from app.repositories.question_repo import Question

class QueryEvaluator:
    """
    Coordinates multi-dataset test case evaluation for submitted SQL queries.
    Compares query results semantically against the reference solution output.
    """

    def evaluate_submission(
        self,
        question: Question,
        submitted_sql: str,
        mode: ExecutionMode = ExecutionMode.READ_ONLY,
    ) -> SubmissionResult:
        executor = db_manager.get_executor(question.database_id)
        test_case_results: List[TestCaseEvaluation] = []
        overall_start = time.perf_counter()

        for tc in question.test_cases:
            tc_start = time.perf_counter()

            # 1. Run reference solution to get the ground truth for this specific dataset
            expected_res: QueryResult = executor.execute_query(
                sql=question.solution_sql,
                custom_seed_dml=tc.custom_seed_dml,
                mode=ExecutionMode.READ_ONLY,
            )

            if not expected_res.success:
                # Instructor solution had an error
                return SubmissionResult(
                    status="INTERNAL_ERROR",
                    all_passed=False,
                    total_test_cases=len(question.test_cases),
                    passed_test_cases=0,
                    execution_time_ms=0.0,
                    error_message=f"Instructor reference query failed on test case '{tc.name}': {expected_res.error}",
                )

            # 2. Run user query on a fresh instance with the same dataset
            user_res: QueryResult = executor.execute_query(
                sql=submitted_sql,
                custom_seed_dml=tc.custom_seed_dml,
                mode=mode,
            )

            tc_elapsed = round((time.perf_counter() - tc_start) * 1000, 2)

            # 3. Check for execution errors (syntax, timeout, restricted operation)
            if not user_res.success:
                status = user_res.error_type or "RUNTIME_ERROR"
                return SubmissionResult(
                    status=status,
                    all_passed=False,
                    total_test_cases=len(question.test_cases),
                    passed_test_cases=len([t for t in test_case_results if t.passed]),
                    execution_time_ms=round((time.perf_counter() - overall_start) * 1000, 2),
                    error_message=user_res.error,
                    test_case_results=test_case_results,
                )

            # 4. Semantic Result Comparison
            validation = evaluate_query_results(
                actual=user_res,
                expected_columns=expected_res.columns,
                expected_rows=expected_res.rows,
                order_matters=question.order_matters,
                check_column_names=question.check_column_names,
            )

            tc_eval = TestCaseEvaluation(
                test_case_id=tc.id,
                name=tc.name,
                is_hidden=tc.is_hidden,
                passed=validation.passed,
                execution_time_ms=tc_elapsed,
                mismatch_reason=(
                    "Hidden test case failed. Output values or row counts did not match expected benchmark."
                    if (tc.is_hidden and not validation.passed)
                    else (validation.reason if not validation.passed else None)
                ),
                # For hidden test cases, protect actual and expected rows from disclosure
                actual_output=(
                    {"columns": user_res.columns, "rows": user_res.rows}
                    if not tc.is_hidden
                    else None
                ),
                expected_output=(
                    {"columns": expected_res.columns, "rows": expected_res.rows}
                    if not tc.is_hidden
                    else None
                ),
            )
            test_case_results.append(tc_eval)

            # Fast fail if a test case fails (like LeetCode) or collect all
            if not validation.passed:
                total_elapsed = round((time.perf_counter() - overall_start) * 1000, 2)
                passed_count = len([t for t in test_case_results if t.passed])
                return SubmissionResult(
                    status="WRONG_ANSWER",
                    all_passed=False,
                    total_test_cases=len(question.test_cases),
                    passed_test_cases=passed_count,
                    execution_time_ms=total_elapsed,
                    test_case_results=test_case_results,
                )

        total_elapsed = round((time.perf_counter() - overall_start) * 1000, 2)
        return SubmissionResult(
            status="ACCEPTED",
            all_passed=True,
            total_test_cases=len(question.test_cases),
            passed_test_cases=len(question.test_cases),
            execution_time_ms=total_elapsed,
            test_case_results=test_case_results,
        )

query_evaluator = QueryEvaluator()

